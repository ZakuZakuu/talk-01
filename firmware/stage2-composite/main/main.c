// SPDX-License-Identifier: MIT
//
// talk.01 bench test, stage 2: ONE USB device that is a MICROPHONE and a KEYBOARD.
//
//   * Microphone: an I2S digital MEMS microphone (ICS-43434 or INMP441 module) read at 48 kHz and sent as 16-bit mono USB audio.
//     The I2S part, the 90 Hz high-pass and the gain shift are adapted from the MIT-licensed project mmajjedi/usb-mic
//     (Copyright (c) 2026 Mahdi), see ../NOTICE.md.
//   * Keyboard: the BOOT button of the board (GPIO0) acts as the push-to-talk key: pressed = the key is held down (Left Alt by default),
//     released = the key is released.
//   * Every 2 seconds the serial monitor shows the microphone level (RMS and peak, in dBFS): a quick look at the silence floor.
//
// UNBUILT AND UNTESTED: written without a compiler or a board. Expect to fix small things. See ../README.md.

#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/i2s_std.h"
#include "esp_log.h"
#include "tusb.h"
#include "usb_device_uac.h"
#include "talk01_usb.h"

static const char *TAG = "talk01";

// ---- wiring (change here if your board does not bring these pins out; any free GPIO works on the S3) ----------------
#define PIN_SCK      4          // microphone SCK  (the I2S bit clock)
#define PIN_WS       5          // microphone WS   (the I2S word select)
#define PIN_SD       6          // microphone SD   (the data)
#define PTT_GPIO     0          // the BOOT button on most ESP32-S3 boards: low when pressed
#define PTT_MODIFIER KEYBOARD_MODIFIER_LEFTALT   // the key held while talking (Alt, for WeChat Input); 0 for none
#define PTT_KEYCODE  0          // an ordinary key to hold as well (0 = none); for example HID_KEY_F13

// ---- audio ------------------------------------------------------------------------------------------------------
#define SAMPLE_RATE  48000      // must match CONFIG_UAC_SAMPLE_RATE in sdkconfig.defaults
#define GAIN_SHIFT   13         // the microphone gives 24 bits in a 32-bit slot; 13 suggested; 12 if too quiet, 14 if it distorts
#define MAX_SAMPLES  1024

static i2s_chan_handle_t rx;
static int32_t raw[MAX_SAMPLES];
// 2nd-order high-pass at 90 Hz, 48 kHz (cuts rumble and DC); coefficients from usb-mic
static const float hb0 = 0.991702f, hb1 = -1.983404f, hb2 = 0.991702f;
static const float ha1 = -1.983335f, ha2 = 0.983477f;
static float hz1 = 0, hz2 = 0;
static volatile bool muted = false;

// level statistics, filled by the microphone callback, printed by stats_task
static volatile double stat_sumsq = 0;
static volatile uint32_t stat_n = 0;
static volatile int16_t stat_peak = 0;

static void i2s_init(void)
{
    i2s_chan_config_t cc = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    ESP_ERROR_CHECK(i2s_new_channel(&cc, NULL, &rx));
    i2s_std_config_t sc = {
        .clk_cfg  = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .mclk = I2S_GPIO_UNUSED, .bclk = PIN_SCK, .ws = PIN_WS,
            .dout = I2S_GPIO_UNUSED, .din = PIN_SD,
        },
    };
    sc.slot_cfg.slot_mask = I2S_STD_SLOT_LEFT;      // the module's L/R pin (or PS pad) selects LEFT: tie it to GND
    ESP_ERROR_CHECK(i2s_channel_init_std_mode(rx, &sc));
    ESP_ERROR_CHECK(i2s_channel_enable(rx));
}

// The host wants microphone data: fill buf with 16-bit mono PCM.
static esp_err_t mic_input_cb(uint8_t *buf, size_t len, size_t *bytes_read, void *ctx)
{
    size_t want = len / sizeof(int16_t);
    if (want > MAX_SAMPLES) want = MAX_SAMPLES;
    size_t got = 0;
    i2s_channel_read(rx, raw, want * sizeof(int32_t), &got, portMAX_DELAY);
    size_t n = got / sizeof(int32_t);
    int16_t *out = (int16_t *)buf;
    double sumsq = 0;
    int16_t peak = 0;
    for (size_t i = 0; i < n; i++) {
        float x = (float)(raw[i] >> GAIN_SHIFT);
        float y = hb0 * x + hz1;
        hz1 = hb1 * x - ha1 * y + hz2;
        hz2 = hb2 * x - ha2 * y;
        if (y > 32767) y = 32767;
        if (y < -32768) y = -32768;
        int16_t s = muted ? 0 : (int16_t)y;
        out[i] = s;
        sumsq += (double)s * (double)s;
        int16_t a = s < 0 ? (int16_t)(-s) : s;
        if (a > peak) peak = a;
    }
    stat_sumsq += sumsq;
    stat_n += (uint32_t)n;
    if (peak > stat_peak) stat_peak = peak;
    *bytes_read = n * sizeof(int16_t);
    return ESP_OK;
}

static esp_err_t spk_output_cb(uint8_t *buf, size_t len, void *ctx) { return ESP_OK; }   // no speaker
static void set_mute_cb(uint32_t mute, void *ctx) { muted = mute; }
static void set_volume_cb(uint32_t vol, void *ctx) { ESP_LOGI(TAG, "host volume %lu", (unsigned long)vol); }

// ---- the callbacks the component would supply, but does not with CONFIG_USB_DEVICE_UAC_AS_PART=y -------------------
void tud_mount_cb(void)   { ESP_LOGI(TAG, "USB mounted"); }
void tud_umount_cb(void)  { ESP_LOGI(TAG, "USB unmounted"); }
void tud_suspend_cb(bool remote_wakeup_en) { (void)remote_wakeup_en; ESP_LOGI(TAG, "USB suspended"); }
void tud_resume_cb(void)  { ESP_LOGI(TAG, "USB resumed"); }

// ---- the push-to-talk key ---------------------------------------------------------------------------------------
static void send_key(bool down)
{
    if (!tud_mounted()) {
        ESP_LOGW(TAG, "key %s ignored: USB not mounted", down ? "down" : "up");
        return;
    }
    for (int i = 0; i < 20 && !tud_hid_ready(); i++) {      // wait up to 100 ms for the HID endpoint
        vTaskDelay(pdMS_TO_TICKS(5));
    }
    uint8_t keycode[6] = {0};
    if (down && PTT_KEYCODE) keycode[0] = PTT_KEYCODE;
    bool ok = tud_hid_keyboard_report(0 /* no report ID */, down ? PTT_MODIFIER : 0, keycode);
    ESP_LOGI(TAG, "key %s %s", down ? "DOWN" : "UP", ok ? "sent" : "NOT SENT");
}

static void ptt_task(void *arg)
{
    gpio_config_t io = {
        .pin_bit_mask = 1ULL << PTT_GPIO,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&io));
    bool pressed = false;
    while (1) {
        bool now = gpio_get_level(PTT_GPIO) == 0;
        if (now != pressed) {
            vTaskDelay(pdMS_TO_TICKS(20));                  // debounce
            now = gpio_get_level(PTT_GPIO) == 0;
            if (now != pressed) {
                pressed = now;
                send_key(pressed);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

// ---- a look at the level ------------------------------------------------------------------------------------------
static void stats_task(void *arg)
{
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(2000));
        double sumsq = stat_sumsq;
        uint32_t n = stat_n;
        int16_t peak = stat_peak;
        stat_sumsq = 0; stat_n = 0; stat_peak = 0;
        if (n == 0) {
            ESP_LOGI(TAG, "level: no audio is being read (the host is not recording)");
            continue;
        }
        double rms = sqrt(sumsq / n);
        double rms_db = rms > 0 ? 20.0 * log10(rms / 32768.0) : -120.0;
        double peak_db = peak > 0 ? 20.0 * log10((double)peak / 32768.0) : -120.0;
        ESP_LOGI(TAG, "level: rms %.1f dBFS, peak %.1f dBFS", rms_db, peak_db);
    }
}

void app_main(void)
{
    i2s_init();
    uac_device_config_t cfg = {
        .output_cb     = spk_output_cb,
        .input_cb      = mic_input_cb,
        .set_mute_cb   = set_mute_cb,
        .set_volume_cb = set_volume_cb,
        .cb_ctx        = NULL,
        .spk_itf_num   = 0,                              // no speaker
        .mic_itf_num   = ITF_NUM_AUDIO_STREAMING_MIC,    // only exists with CONFIG_USB_DEVICE_UAC_AS_PART=y
    };
    ESP_ERROR_CHECK(uac_device_init(&cfg));
    xTaskCreate(ptt_task, "ptt", 3072, NULL, 5, NULL);
    xTaskCreate(stats_task, "stats", 3072, NULL, 3, NULL);
    ESP_LOGI(TAG, "talk.01 bench ready: microphone + keyboard (BOOT button = push to talk)");
}
