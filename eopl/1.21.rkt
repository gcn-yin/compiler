;; Exercise 1.21
(define product-old
  (lambda (first second)
    (if (eqv? first '())
        '()
        (cons (product-aux (car first) second)
              (product-old (cdr first) second)))))

(define product
  (lambda (first second)
    (product-aux2 (product-old first second))))

(define product-aux
  (lambda (ele alist)
    (if (eqv? alist '())
        '()
        (cons (list ele (car alist))
              (product-aux ele (cdr alist))))))

(define product-aux2
  (lambda (alist)
    (let ((new-list (flatten alist)))
      (if (eqv? new-list '())
          '()
          (cons (list (car new-list)
                      (cadr new-list))
                (product-aux2 (cddr new-list)))))))