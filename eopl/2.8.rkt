;; Exercise 2.8
(define empty-env?
  (lambda (env)
    (if (eqv? (car env) 'empty-env)
        #t
        #f)))