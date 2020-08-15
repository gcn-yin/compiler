;; Exercise 1.15
(define duple
  (lambda (n x)
    (if (eqv? n 0)
        '()
        (if (eqv? n 1)
            (cons x '())
            (cons x (duple (- n 1) x))))))