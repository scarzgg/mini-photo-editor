"""Mini photo editor: load an image, apply effects with key presses.

Controls: g = grayscale | b = blur | e = edges | r = reset | s = save | q = quit
"""

import cv2
from pathlib import Path

path = input("Drag an image into this window and press Enter: ").strip().strip('"').strip("'")

original = cv2.imread(path)
if original is None:
    raise SystemExit(f"Could not read image: {path}")

current = original.copy() # .copy() so edits dont affect original image - which 'r' needs
print("g = grayscale | b = blur | e = edges | r = reset | s = save | q = quit")

while True:
    cv2.imshow("Editor", current)
    key = cv2.waitKey(0) & 0xFF

    if key == ord("g"):
        gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY) # change to 1 channel for gray, return to 3 channel below so other edits work
        current = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) # return shape back to (h,w,3)
    elif key == ord("b"):
        current = cv2.GaussianBlur(current, (15,15), 0)
    elif key == ord("e"):
        gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY) # canny needs 1 channel
        edges = cv2.Canny(gray, 100, 200) # 100/200 are the lower/upper thresholds
        current = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR) # return to 3 channel shape so other edits work
    elif key == ord("r"):
        current = original.copy()
    elif key == ord("s"):
        out = Path(path).with_name(Path(path).stem + "_edited.jpg")
        cv2.imwrite(str(out), current)
        print(f"Saved to: {out}")
    elif key == ord("q"):
        break


cv2.destroyAllWindows()