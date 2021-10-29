#lang scheme
;2016400123
;ALGI KANAR
;-------------------------------------------------------------------------

;I divide the function into two.DELIVERY-COST is sending necessary information to deliverycost2.
;Then,deliverycost2 is traversing the BAKERIES list using the length of it as a termination condition.
;When it finds the the bakery that we want it returns the cost of that bakery by tearing the list into necessary pieces.
;b->bakery
;y->bakery, bake->BAKERIES list, len->BAKERIES list length

(define (deliverycost2 y bake len)
  (if (eqv? len 0)
      (display 0)
      (if(eqv?(car(car bake)) y)
         (display(car(cdr(car bake))))
         (deliverycost2 y (cdr bake)(- len 1)))))

(define (DELIVERY-COST b)
  (deliverycost2 b BAKERIES (length BAKERIES)))
;-------------------------------------------------------------------------

;I divide the function into two.GOODS-AVAILABLE is sending necessary information to goodsavailable2.
;Then,goodsavailable2 is traversing the BAKERIES list using the length of it as a termination condition.
;When it finds the the goods list that we want it returns the currently produced goods of that bakery by tearing the list into necessary pieces.
;b->bakery.
;y->bakery, bake->BAKERIES list, len->BAKERIES list length.

(define (goodsavailable2 y bake len)
  (if (eqv? len 0)
      (display '())
      (if(eqv?(car(car bake)) y)
         (display(car(cdr(cdr(car bake)))))
         (goodsavailable2 y (cdr bake)(- len 1)))))

(define (GOODS-AVAILABLE b)
  (goodsavailable2 b BAKERIES (length BAKERIES)))
;-------------------------------------------------------------------------

;I divide the function into two.GOODS-INTERESTED is sending necessary information to goodsinterested2.
;Then,goodsinterested2 is traversing the HOTELS list using the length of it as a termination condition.
;When it finds the the goods list that we want it returns the currently anticipated goods of that hotel by tearing the list into necessary pieces.
;h->hotel.
;x->hotel, hot->HOTELS list, len->HOTELS list length.

(define (goodsinterested2 x hot len)
  (if (eqv? len 0)
      (display '())
      (if(eqv?(car(car hot)) x)
         (display (car(cdr(cdr(car hot)))))
         (goodsinterested2 x (cdr hot)(- len 1)))))

(define (GOODS-INTERESTED h)
  (goodsinterested2 h HOTELS (length HOTELS)))
;-------------------------------------------------------------------------

;I divide the function into two.AGREED-BAKERIES is sending necessary information to agreedbakeries2.
;Then,bakeries2 is traversing the HOTELS list using the length of it as a termination condition.
;When it finds the the bakeries list that we want it returns the bakeries that are under contract of that hotel by tearing the list into necessary pieces.
;h->hotel.
;x->hotel, hot->HOTELS list, len->HOTELS list length

(define (agreedbakeries2 x hot len)
  (if (eqv? len 0)
      (display '())
      (if(eqv?(car(car hot)) x)
         (display (car(cdr(car hot))))
         (agreedbakeries2 x (cdr hot)(- len 1)))))

(define (AGREED-BAKERIES h)
  (agreedbakeries2 h HOTELS (length HOTELS)))
;-------------------------------------------------------------------------

;member function is used for to understand whether a certain element resides in a list and it returns a boolean according to the answer.
;This function would be helpful in the later functions.
;el->element that we want to check, lst->the list that may or may not keeping the element we want. 

(define (member el lst)
    (cond
        ((null? lst) #F)
        ((eq? el (car lst)) #T)
        (else (member el (cdr lst)))))
;-------------------------------------------------------------------------

;append function is used for to merge given lists and returns as a single list.
;This function would be helpful in the later functions.
;list1->first list that we want to merge, list2->second list that we want to merge.

(define (append list1 list2)
        (if (null? list1) list2
            (cons (car list1) (append (cdr list1) list2))))
;-------------------------------------------------------------------------

;I divide the function into two.AGREED-HOTELS is sending necessary information to agreedhotels2 and it is initializing an empty list in order to fill it with matching hotels.
;Then,agreedhotels2 is processing the info by looking up the bakerylist inside the HOTELS.After this, if the list contains the bakery we send as a parameter, by using member function  
;it fills the formerly emptylist via recursion,the list will contain all the hotels we look for at the time len becomes 0 which is the termination condition.
;b->bakery.
;x->hotel, hot->HOTELS list, len->HOTELS list length, li->list we are filling.

(define (agreedhotels2 x hot len li) 
  (cond
      [(eqv? len 0) (display li)]
      [(member x (car(cdr(car hot))))(agreedhotels2 x (cdr hot)(- len 1)(append li (list(car(car hot)))))]
      [else(agreedhotels2 x (cdr hot) (- len 1) li )]))
 

(define (AGREED-HOTELS b)
  (agreedhotels2 b HOTELS (length HOTELS) '()))
;-------------------------------------------------------------------------

;I divide the function into two.BOUGHT-BY is sending necessary information to boughtby2 and it is initializing an empty list in order to fill it with matching hotels.
;Then,agreedhotels2 is processing the info by looking up the goodslist inside the HOTELS.After this, if the list contains the good we send as a parameter, by using member function  
;it fills the formerly emptylist via recursion,the list will contain all the hotels we look for at the time len becomes 0 which is the termination condition.
;g->good.
;z->good, hot->HOTELS list, len->HOTELS list length, li->list we are filling.

(define (boughtby2 z hot len li)
  (cond
      [(eqv? len 0) (display li)]
      [(member z (car(cdr(cdr(car hot)))))(boughtby2 z (cdr hot)(- len 1)(append li (list(car(car hot)))))]
      [else(boughtby2 z (cdr hot) (- len 1) li )]))
 
(define (BOUGHT-BY g)
  (boughtby2 g HOTELS (length HOTELS) '()))
;-------------------------------------------------------------------------

;8 definitions under this comment are same with their above conterparts.Since I'm using display in functions,I redefined them
;and slightly changed their names in order to avoid any unnecessary display when using them in the last 4 main functions.

(define (goodsavailableB y bake len)
  (if (eqv? len 0)
      '()
      (if(eqv?(car(car bake)) y)
         (car(cdr(cdr(car bake))))
         (goodsavailableB y (cdr bake)(- len 1)))))

(define (goodsavailableA b)
  (goodsavailableB b BAKERIES (length BAKERIES)))

(define (deliverycostB y bake len)
  (if (eqv? len 0)
      0
      (if(eqv?(car(car bake)) y)
         (car(cdr(car bake)))
         (deliverycostB y (cdr bake)(- len 1)))))

(define (Delivery-CostA b)
  (deliverycostB b BAKERIES (length BAKERIES)))

(define (goodsinterestedB x hot len)
  (if (eqv? len 0)
      '()
      (if(eqv?(car(car hot)) x)
         (car(cdr(cdr(car hot))))
         (goodsinterestedB x (cdr hot)(- len 1)))))

(define (Goods-InterestedA h)
  (goodsinterestedB h HOTELS (length HOTELS)))

(define (agreedbakeriesB x hot len)
  (if (eqv? len 0)
      '()
      (if(eqv?(car(car hot)) x)
         (car(cdr(car hot)))
         (agreedbakeriesB x (cdr hot)(- len 1)))))

(define (Agreed-BakeriesA h)
  (agreedbakeriesB h HOTELS (length HOTELS)))
;-------------------------------------------------------------------------

;I divide the function into two.Best-PRICE is sending necessary information to bestprice2 and it is initializing an empty list in order to fill it with possible prices for the good.
;Then,bestprice2 is processing the info by looking up the prices inside the GOODS.Putting all the possible price values for the good we want,
;it is sorting the list starting from least.Following that, displaying the first element of the list when the termination conditon len hits 0.
;This function also looks for whether the good is available by the bakery right now.
;g->good.
;z->good, god->GOODS list, len->GOODS list length, li->list we are filling.

(define (bestprice2 z god len li)
  
  (cond
      [(and(eqv? len 0)(null? li))(display '())]
      [(and(eqv? len 0)(not(null? li))) (display (car(sort li <)))]
      [(and(eqv? z (car(car god)))(member z (goodsavailableA(cadar god))))(bestprice2 z (cdr god)(- len 1)(append li (cdr(cdr(car god)))))]
      [else(bestprice2 z (cdr god) (- len 1) li )]))
 

(define (BEST-PRICE g)
  (bestprice2 g GOODS (length GOODS) '()))
;-------------------------------------------------------

;I divide the function into three.TOTAL-COST-GOOD is sending the necessary info and an emty list.In totalcost2 if the hotel we give doesn't need the good
;since it is an unwanted good it will display 0.However;if the hotel needs the good it will pass the totalcost2 check point and begin to look for the possible costs
;with searching function.Searching function will traverse the GOODS list and when it finds the good it should also need to look at the corresponding bakery.The reason is that
;the bakery may not be selling the good at that time of being.After calculating the totalcost by adding the price and deliverycost it recursively puts them into the list.
;When len hit 0, it will sort that list and display the first element(the min cost) of the list as the result.
;h->hotel, g->good.
;x->good, hot->hotel, hotlis->HOTELS list, totlis->the list we will fill possible totalcosts.
;x->good, god->GOODS list, lis->hotel's agreed bakeries list, len->length of GOODS list, totlis->the list we will fill possible totalcosts.

(define (searching x god lis len totlis)
  (cond
    [(and(eqv? len 0)(null? totlis))(display 0)]
    [(and(eqv? len 0)(not(null? totlis)))(display (car(sort totlis <)))]
    [(and(and(eqv? x (caar god))(member (cadar god)lis))(member x (goodsavailableA(cadar god))))(searching x (cdr god)lis(- len 1)(append totlis (list(+(car(sort(cddar god)<))(Delivery-CostA (cadar god))))))]
    [else(searching x (cdr god)lis (- len 1)totlis)]))

(define (totalcost2 x hot hotlis totlis)
  (cond
    [ (member x (Goods-InterestedA hot))(searching x GOODS (Agreed-BakeriesA hot)(length GOODS)totlis)]
    [else (display 0)]))

(define (TOTAL-COST-GOOD h g)
  (totalcost2 g h HOTELS '()))
;-------------------------------------------------------------------------

;TOTAL-COST-LIST is implementing the same principles used in TOTAL-COST-GOOD.Only difference is that
;now it needs to find minimum cost for each of the goods in the hotel's goods list which are currently available in the bakery.
;Therefore, I modified the previous searching function by putting a result parameter.
;The min totalcosts will be add up recursively.When len hit 0,result will be displayed.
;h->hotel.
;h->hotel, len->length of the list of goods interested by the hotel, lis->the list of goods interested by the hotel, res->the min total cost of all goods will be stored here.
;parameters for the rest are same as the TOTAL-COST-GOOD since it is the displayless version of it except the result part.


(define (searchingA x god lis len totlis result)
  (cond
    [(and(eqv? len 0)(null? totlis))0]
    [(and(eqv? len 0)(not(null? totlis)))(+ result(car(sort totlis <)))]
    [(and(and(eqv? x (caar god))(member (cadar god)lis))(member x (goodsavailableA(cadar god))))(searchingA x (cdr god)lis(- len 1)(append totlis (list(+(car(sort(cddar god)<))(Delivery-CostA (cadar god)))))result)]
    [else(searchingA x (cdr god)lis (- len 1)totlis result)]))

(define (totalcostB x hot hotlis totlis result)
  (cond
    [ (member x (Goods-InterestedA hot))(searchingA x GOODS (Agreed-BakeriesA hot)(length GOODS)totlis result)] ))

(define (Total-Cost-GoodA g h)
  (totalcostB g h HOTELS '() 0))

(define(totalcostlist2 h len lis res )
  (cond
    [(eqv? len 0)(display res)]
    [else (totalcostlist2 h (- len 1)(cdr lis)(+ res (Total-Cost-GoodA (car lis) h)))]))

(define(TOTAL-COST-LIST h)
  (totalcostlist2 h (length(Goods-InterestedA h))(Goods-InterestedA h) 0))
;-------------------------------------------------------------------------

;I divide the function into three.WITHIN-BUDGET will control whether the numbers given are ordered from min to max.If it is,it will go to withinbuget2.
;Until it reaches the maximum price value it will go into withinbudget3.Withinbudget3 will collect the list 'containing suitable good and bakery combinations'.
;The budget we are looking for changes in every iteration.Because of that,when the current budget value is equal to the price in the searched list,
;it will fill the list that sent as a parameter recursively.
;At the time it reaches to max value after the last iteration, it will display the list filled with combinations in sorted manner(since we start from min and went up one by one).
;This function also looks for whether the good is available by the bakery right now.
;mi->min price value, ma->max price value
;mi->min price value, ma->max price value, li->the list we ar filling with suitable good and bakery combinations.
;mi->min price value, ma->max price value, god->GOODS list, len->length of GOODS lis,t li->the list we ar filling with suitable good and bakery combinations.

(define (withinbudget3 mi ma god len li)
  (cond
      [(eqv? len 0) li ]
      [(and(eqv? mi (car(cdr(cdr(car god)))))(member(car(car god))(goodsavailableA(cadar god))))(withinbudget3 mi ma (cdr god)(- len 1)(append li (list(append (list(caar god))(list(cadar god))))))]
      [else(withinbudget3 mi ma (cdr god) (- len 1) li )]))
 
(define (withinbudget2 mi ma li)
  (cond
    [(eqv? (- mi 1) ma)(display li)]
    [else(withinbudget2 (+ mi 1) ma (append li (withinbudget3 mi ma GOODS (length GOODS) '())))]))

(define (WITHIN-BUDGET mi ma) 
   (if(> mi ma)(display "Wrong ordered arguments!")(withinbudget2 mi ma '())))
;-----------------------------------FIN----------------------------------------------