;; Exercise 1.19
(define list-set
  (lambda (lst n x)
    (if (eqv? n 0)
        (cons x (cdr lst))
        (cons (car lst)
              (list-set (cdr lst) (- n 1) x)))))