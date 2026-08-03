;; Auto-generated PDDL Problem
;; Generated: 2026-03-10T11:55:46.791058
;; Targets detected: 1

(define (problem vlm_generated_20260310_115546)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    blue_box_0012 - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: blue_box_0012
    (= (tx blue_box_0012) 0.9)
    (= (ty blue_box_0012) 0.35)
    (= (tz blue_box_0012) 0.05)

  )

  (:goal
    (and
      (fly_to blue_box_0012)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)