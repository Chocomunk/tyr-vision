# videooverlay.py
#
# Module for rendering HUD overlay on the video

import cv2

import serialoutput
import targeting
import videoinput


def draw_goal(frame, target):
    """ Given the target contour, draws the extrapolated goal shape. """

    x,y,w,h = cv2.boundingRect(target)  # find a non-rotated bounding rectangle
    #cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)  # draw bounding rectangle in green

    # Draw goal contour based on the bounding box
    tape_x = int(w/10)
    tape_y = int(h/7)
    goal_x = x+tape_x
    goal_y = y-h+tape_y
    goal_w = int(w*4/5)
    goal_h = int(h*12/7)
    # circle parameters
    radius = int(goal_w/2)
    center = (goal_x+radius, goal_y+radius)
    cv2.rectangle(frame, (goal_x, goal_y+radius), (goal_x+goal_w, goal_y+goal_h), (255, 0, 255), -1)  # draw the goal bounding box in purple
    cv2.circle(frame, center, radius, (255, 0, 255), -1)


def draw_base_HUD(frame):
    """ Draw base crosshairs in black on the given frame. Returns the frame's
    center coordinate. """
    center_x, center_y = targeting.image_center(frame)

    cv2.line(frame, (center_x, 0), (center_x, videoinput.frame_height), (0, 0, 0), 2) # Vertical line
    cv2.line(frame, (0, center_y), (videoinput.frame_width, center_y), (0, 0, 0), 2) # Horizontal line
    cv2.circle(frame, (center_x, center_y), 25, (0, 0, 0), 2) # center circle
    return center_x, center_y


# TODO: ser should not be passed to this function!
def draw_targeting_HUD(frame, target):
    """ Draws the target, goal (via the draw_goal() function),
    displacement vector, and a text box showing the target's displacement. """

    cv2.rectangle(frame, (0, 0), (320, 48), (0, 0, 0), -1) # Rectangle where text will be displayed
    if target is None:
        cv2.putText(frame, "No target found", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        serialoutput.send_data("No target")
    else:  # draw the best match and its bounding box
        cv2.drawContours(frame, [target], 0, (255, 255, 0), 3) # Draw target in cyan
        draw_goal(frame, target)

        center_x, center_y = targeting.image_center(frame)
        target_x, target_y = targeting.target_center(target)

        # Show the displacement as a vector in Cartesian coordinates (green)
        displacement_x = target_x - center_x # Positive when to the right of center
        displacement_y = center_y - target_y # Positive when above center
        cv2.line(frame, (center_x, center_y), (target_x, target_y), (0, 255, 0), 5)
        # Overlay the displacement values as text
        text = "<%d, %d>" % (displacement_x, displacement_y)
        cv2.putText(frame, "%s" % text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        # Get bounding box dimensions
        #_, _, width, height = cv2.boundingRect(target) # Standard
        _, (width, height), _ = cv2.minAreaRect(target) # Rotated
        # Send displacement data over serial
        serialoutput.send_data(displacement_x, displacement_y, int(width), int(height))


def draw_fps(frame, fps):
    """ Draws the given framerate onto the given frame """
    cv2.rectangle(frame, (0, 48), (320, 96), (0, 0, 0), -1)
    cv2.putText(frame, "FPS: %f" % fps, (16, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
