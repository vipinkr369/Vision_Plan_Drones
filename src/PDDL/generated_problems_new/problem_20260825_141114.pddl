;; Auto-generated PDDL Problem
;; Generated: 2026-08-25T14:11:14.314417
;; Targets detected: 1

(define (problem vlm_generated_20260825_141114)
  (:domain warehouse-drone)

  (:objects
    drone1 - drone
    red_box_001 - target
  )

  (:init
    (landed drone1)

    ;; Drone initial position
    (= (x drone1) 0.0)
    (= (y drone1) 0.0)
    (= (z drone1) 0.0)

    ;; Target: red_box_001
    (= (tx red_box_001) 2.776)
    (= (ty red_box_001) -1.887)
    (= (tz red_box_001) 4.521)

  )

  (:goal
    (and
      (scanned red_box_001)
      (landed drone1)
    )
  )

  (:metric minimize (total-time))
)