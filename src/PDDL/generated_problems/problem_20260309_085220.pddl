;; Auto-generated PDDL Problem
;; Generated: 2026-03-09T08:52:20.079246
;; Targets detected: 1

(define (problem vlm_generated_20260309_085220)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    box - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: box
    (= (tx box) 13.9)
    (= (ty box) -0.01)
    (= (tz box) 0.1)

  )

  (:goal
    (and
      (scanned box)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)