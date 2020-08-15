;; Exercise 1.20
(define count-occurrences
  (lambda (s slist)
    (sum (map (lambda (x)
                (if (symbol? x)
                    (if (eqv? x s) 1 0)
                    (count-occurrences s x)))
            slist))))

(define sum
  (lambda (lst)
    (if (eqv? lst '())
        0
        (+ (car lst) (sum (cdr lst))))))