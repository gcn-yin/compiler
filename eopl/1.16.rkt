;; Exercise 1.16
(define invert
  (lambda (lst)
    (map (lambda (x) (list (cadr x) (car x)))
         lst)))