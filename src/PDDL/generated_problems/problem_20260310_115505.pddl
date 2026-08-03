;; Auto-generated PDDL Problem
;; Generated: 2026-03-10T11:55:05.440152
;; Targets detected: 0

(define (problem vlm_generated_20260310_115505)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

  )

  (:goal
    (and
      (fly_to yellow_box_0012)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)