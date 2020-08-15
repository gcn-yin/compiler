;; Exercise 1.18
(define swapper
  (lambda (s1 s2 slist)
    (map (lambda (ele)
           (if (symbol? ele)
               (cond ((eqv? ele s1) s2)
                     ((eqv? ele s2) s1)
                     (else ele))
               (swapper s1 s2 ele)))
         slist)))