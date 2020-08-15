;; Exercise 1.22
(define filter-in
  (lambda (pred lst)
    (if (eqv? lst '())
        '()
        (let ((first (car lst)))
          (if (pred first)
              (cons first (filter-in pred (cdr lst)))
              (filter-in pred (cdr lst)))))))