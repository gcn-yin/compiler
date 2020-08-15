;; Exercise 2.21
(define-datatype env-exp env-exp?
  (empty-env)
  (extend-env
   (identifier identifier?)
   (value number?)
   (old-env env-exp?)))

(define has-binding?
  (lambda (env s)
    (cases env-exp env
      (empty-env () #f)
      (extend-env
       (identifier value old-env)
       (or (eqv? identifier s)
           (has-binding? old-env))))))