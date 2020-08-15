;; Exercise 1.17
(define down
  (lambda (lst)
    (map (lambda (x) (list x))
         lst)))