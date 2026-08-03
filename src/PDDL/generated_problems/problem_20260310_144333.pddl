;; Auto-generated PDDL Problem
;; Generated: 2026-03-10T14:43:33.335329
;; Targets detected: 1

(define (problem vlm_generated_20260310_144333)
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
    (= (tx box) 45.68)
    (= (ty box) 58.42)
    (= (tz box) 2.55)

  )

  (:goal
    (and
      (scanned box)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)