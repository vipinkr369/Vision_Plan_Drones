;; Auto-generated PDDL Problem
;; Generated: 2026-03-09T08:36:14.107684
;; Targets detected: 0

(define (problem vlm_generated_20260309_083614)
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
      (scanned box)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)