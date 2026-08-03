;; Auto-generated PDDL Problem
;; Generated: 2026-03-10T14:13:45.200530
;; Targets detected: 1

(define (problem vlm_generated_20260310_141345)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    red_box_0008 - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: red_box_0008
    (= (tx red_box_0008) 46.01)
    (= (ty red_box_0008) 57.61)
    (= (tz red_box_0008) 2.07)

  )

  (:goal
    (and
      (fly_to red_box_0008)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)