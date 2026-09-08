;; Auto-generated PDDL Problem
;; Generated: 2026-09-07T14:40:09.474889
;; Targets detected: 1

(define (problem vlm_generated_20260907_144009)
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
    (= (tx forklift_001) 1.72)
    (= (ty forklift_001) -0.606)
    (= (tz forklift_001) 4.596)

  )

  (:goal
    (and
      (scanned forklift_001)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)