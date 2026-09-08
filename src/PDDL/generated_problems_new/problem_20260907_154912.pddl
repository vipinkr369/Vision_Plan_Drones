;; Auto-generated PDDL Problem
;; Generated: 2026-09-07T15:49:12.605981
;; Targets detected: 1

(define (problem vlm_generated_20260907_154912)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    forklift_001 - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: forklift_001
    (= (tx forklift_001) -1.926)
    (= (ty forklift_001) -4.719)
    (= (tz forklift_001) 0.392)

  )

  (:goal
    (and
      (scanned forklift_001)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)