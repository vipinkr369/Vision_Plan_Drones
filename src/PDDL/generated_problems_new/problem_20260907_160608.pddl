;; Auto-generated PDDL Problem
;; Generated: 2026-09-07T16:06:08.883374
;; Targets detected: 1

(define (problem vlm_generated_20260907_160608)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    green_box_001 - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: green_box_001
    (= (tx green_box_001) 0.492)
    (= (ty green_box_001) -3.383)
    (= (tz green_box_001) 0.555)

  )

  (:goal
    (and
      (scanned green_box_001)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)