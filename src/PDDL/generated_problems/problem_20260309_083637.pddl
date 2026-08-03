;; Auto-generated PDDL Problem
;; Generated: 2026-03-09T08:36:37.115846
;; Targets detected: 1

(define (problem vlm_generated_20260309_083637)
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
    (= (tx box) 12.51)
    (= (ty box) 5.3)
    (= (tz box) 1.5)

  )

  (:goal
    (and
      (scanned box)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)