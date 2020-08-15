;; Exercise 1.13
(define subst-1-13
  (lambda (new old slist)
    (if (null? slist)
        '()
        (map (lambda (ele)
               (if (and (symbol? ele)
                        (eqv? ele old))
                   new
                   (subst-1-13 new old ele)))
             slist))))