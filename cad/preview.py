# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Shaded previews of the STL files with a small z-buffer renderer (numpy + matplotlib for the image), so the shapes can be looked at
without a CAD viewer.
    python3 cad/preview.py
"""
import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def rot(elev, azim):
    e, a = np.radians(elev), np.radians(azim)
    rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return rx @ rz


def render(mesh, elev, azim, px=520, color=(0.86, 0.80, 0.66), pad=1.08, span=None):
    """Orthographic z-buffer render. The viewer looks along -Z' after rotating by (elev, azim); returns an RGB image."""
    R = rot(elev, azim)
    v = (mesh.vertices - mesh.bounds.mean(axis=0)) @ R.T
    tris = v[mesh.faces]
    nrm = mesh.face_normals @ R.T
    r = (span or (mesh.bounds[1] - mesh.bounds[0]).max()) * pad / 2
    sx = (tris[:, :, 0] / r * 0.5 + 0.5) * (px - 1)
    sy = (1 - (tris[:, :, 1] / r * 0.5 + 0.5)) * (px - 1)
    z = tris[:, :, 2]
    img = np.ones((px, px, 3)) * 0.96
    zb = np.full((px, px), -1e9)
    light = np.array([0.35, 0.55, 0.75]); light /= np.linalg.norm(light)
    for i in range(len(tris)):
        if nrm[i, 2] < -0.02:
            continue
        x0, y0, x1, y1, x2, y2 = sx[i, 0], sy[i, 0], sx[i, 1], sy[i, 1], sx[i, 2], sy[i, 2]
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-9:
            continue
        xa, xb = int(max(0, np.floor(min(x0, x1, x2)))), int(min(px - 1, np.ceil(max(x0, x1, x2))))
        ya, yb = int(max(0, np.floor(min(y0, y1, y2)))), int(min(px - 1, np.ceil(max(y0, y1, y2))))
        if xb < xa or yb < ya:
            continue
        gx, gy = np.meshgrid(np.arange(xa, xb + 1), np.arange(ya, yb + 1))
        l0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) / den
        l1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) / den
        l2 = 1 - l0 - l1
        m = (l0 >= -1e-4) & (l1 >= -1e-4) & (l2 >= -1e-4)
        if not m.any():
            continue
        zz = l0 * z[i, 0] + l1 * z[i, 1] + l2 * z[i, 2]
        sel = m & (zz > zb[gy, gx])
        zb[gy[sel], gx[sel]] = zz[sel]
        shade = 0.30 + 0.70 * max(0.0, float(nrm[i] @ light))
        img[gy[sel], gx[sel]] = np.array(color) * shade
    return img


def sheet(items, path, title, cols=None):
    cols = cols or len(items)
    rows = (len(items) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols, 4.8 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (mesh, elev, azim, label, kw) in zip(axes, items):
        ax.imshow(render(mesh, elev, azim, **kw))
        ax.set_title(label, fontsize=10)
        ax.axis("off")
    for ax in axes[len(items):]:
        ax.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def main():
    asm = trimesh.load(os.path.join(OUT, "mockup_assembled_view.stl"))
    # the body's local axes: x right, y up, z toward the viewer; azim/elev below tilt it
    sheet([(asm, 0, 0, "front", {}), (asm, -35, 25, "three-quarter (from below-left)", {}), (asm, 0, 90, "from the left (the key side)", {}), (asm, -90, 0, "from the top edge", {})],
          os.path.join(OUT, "preview_mockup.png"), "Feel mock-up: body + 5 mm key + wheel (assembled view)")
    lid = trimesh.load(os.path.join(OUT, "snap_lid.stl"))
    frame = trimesh.load(os.path.join(OUT, "snap_frame.stl"))
    plate = trimesh.load(os.path.join(OUT, "calibration_plate.stl"))
    sheet([(lid, -50, 20, "snap lid (seen from the front, tilted)", {}), (frame, -50, 20, "snap frame (front, tilted)", {}), (plate, -55, 15, "calibration plate (front, tilted)", {"px": 700})],
          os.path.join(OUT, "preview_calibration.png"), "Calibration set (the lid is printed back down, the frame and the plate face up)")
    try:
        sh = trimesh.load(os.path.join(OUT, "s2_lower_shell.stl"))
        ld = trimesh.load(os.path.join(OUT, "s2_lid.stl"))
        asm = trimesh.load(os.path.join(OUT, "s2_lower_assembled_view.stl"))
        sheet([(sh, 0, 0, "shell, front", {"px": 640}), (sh, -45, 15, "shell, tilted", {"px": 640}), (ld, -45, 15, "lid, tilted", {"px": 640}), (asm, -45, 15, "lid in the shell", {"px": 640})],
              os.path.join(OUT, "preview_s2_lower.png"), "S2 lower shell with the real lid (hooks at the top, snap arms in the side rails, finger slot at the chin)")
    except Exception as e:
        print("s2 preview skipped:", e)
    try:
        sh = trimesh.load(os.path.join(OUT, "s2_cap_shell.stl"))
        cp = trimesh.load(os.path.join(OUT, "s2_cap.stl"))
        asm = trimesh.load(os.path.join(OUT, "s2_cap_assembled_view.stl"))
        sheet([(cp, -50, 20, "cap: the face (one plain plane, ridges, no catches)", {"px": 640}), (cp, 130, 20, "cap: the back (four pegs, the detent groove)", {"px": 640}),
               (sh, -50, 20, "shell: floor with keyholes, the detent tongue, the round hole", {"px": 640}), (asm, -50, 20, "cap locked on the shell", {"px": 640})],
              os.path.join(OUT, "preview_s2_cap.png"), "S2 keyhole-slide cap: nothing shows on the face", cols=2)
    except Exception as e:
        print("s2 cap preview skipped:", e)
    try:
        fp = trimesh.load(os.path.join(OUT, "s2_frame_PRINT_front_down.stl"))
        fa = trimesh.load(os.path.join(OUT, "s2_frame_assembled_view.stl"))
        cp2 = trimesh.load(os.path.join(OUT, "s2_cap_PRINT_face_down.stl"))
        sheet([(fp, 0, 0, "frame as printed, seen from above (the open back, the bosses, the mic seat)", {"px": 640}), (fp, -50, 20, "frame as printed, tilted", {"px": 640}),
               (fa, -50, 20, "assembled: the cap on the frame, with the stop bar", {"px": 640}), (cp2, 130, 20, "cap as printed (front face down, pegs up)", {"px": 640})],
              os.path.join(OUT, "preview_s2_frame.png"), "S2 lower frame, printed FRONT FACE DOWN, no supports", cols=2)
    except Exception as e:
        print("frame preview skipped:", e)
    try:
        asm = trimesh.load(os.path.join(OUT, "s2_body_assembled_view.stl"))
        opn = trimesh.load(os.path.join(OUT, "s2_body_open_view.stl"))
        up = trimesh.load(os.path.join(OUT, "s2_upper_PRINT_front_down.stl"))
        bk = trimesh.load(os.path.join(OUT, "s2_back_PRINT_outer_face_up.stl"))
        sheet([(asm, -50, 20, "the body, front (frame + upper shell + cap + back plate + a plain wheel)", {"px": 640}), (asm, 130, 20, "the body, back (7 countersunk screws)", {"px": 640}),
               (opn, 140, 35, "without the back plate and cap: the board pocket, the tube, the bosses", {"px": 640}), (up, 0, 0, "upper shell as printed, from above", {"px": 640}),
               (up, -50, 25, "upper shell as printed, tilted", {"px": 640}), (bk, 0, 0, "back plate as printed (outer face up)", {"px": 640})],
              os.path.join(OUT, "preview_s2_body.png"), "S2 body: lower frame + upper shell + back plate", cols=2)
    except Exception as e:
        print("body preview skipped:", e)
    print("previews written")


if __name__ == "__main__":
    main()
