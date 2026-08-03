;; Auto-generated PDDL Problem
;; Generated: 2026-03-09T09:30:15.365359
;; Targets detected: 1

(define (problem vlm_generated_20260309_093015)
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
    (= (tx blue_box_0012) 13.9)
    (= (ty blue_box_0012) -3.84)
    (= (tz blue_box_0012) 3.6)

  )

  (:goal
    (and
      (fly_to blue_box_0012)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)