;; Exercise 2.9
(define has-binding?
  (lambda (env search-var)
    (cond ((eqv? (car env) 'empty-env)
           #f)
          ((eqv? (car env) 'extend-env)
           (let ((saved-var (cadr env))
                 (saved-val (caddr env))
                 (saved-env (cadddr env)))
             (if (eqv? search-var saved-var)
                 #t
                 (has-binding? saved-env search-var))))
          (else #f))))