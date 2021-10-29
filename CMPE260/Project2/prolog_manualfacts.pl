% These are used for the evaluations of the clues that consits of the phrases like either or one of the.
% As the name suggests these work as logical operators.
% Also I used a built-in logic operator 'not' in other deductions(not(:Goal)).
% and(+[H])
% and(+[H|T])
% or(+[H])
% or(+[H|_])
% or(+[_|T])
and([H]) :- H.
and([H|T]) :- H, and(T).
or([H]) :- H,!.
or([H|_]) :- H,!.
or([_|T]) :- or(T).

% Before mentioning all the clues one by one,I want to give the purpose of the 'member' in general.
% For the clues that are linked to shipments which are matched with customers, since we used customers as 
% pivots we don't need to control them with 'member', we just need to directly check them with the info yet for
% the shipments that are not matched with a certain person we have to look for whether it is matchable with a customer by 'member'.

% Neither the package with the television in it nor hayriye’s package is the shipment going to beykoz.
% In neither phrases the information given in the left hand side of the clue can coincide if both of them follows the right hand side.
% Therefore I didn't put any restriction which prohibits this possibility.(This also applies for the clue7)
% C1_t is a dummy location for tv shipment.
% clue1(+H_t(Hayriye town),+Customers)
clue1(H_t,Customers):-
member([tv,C1_t,_], Customers),
not(C1_t = beykoz),
not(H_t = beykoz).

% The shipment with the television in it cost 1 lira more than the package going to uskudar.
% C2_p1 and C2_p2 are dummy prices for tv shipment and uskudar shipment.
% It uses arithmetic operation to see whether it achieves the condition.
% clue2(+Customers)
clue2(Customers):-
member([tv,_,C2_p1], Customers),
member([_,uskudar,C2_p2], Customers),
C2_p1 - C2_p2 =:= 1.

% The shipment with the basketball in it didn’t cost 9.
% C3_p is a dummy price for basketball shipment.
% clue3(+Customers)
clue3(Customers):-
member([basketball,_,C3_p], Customers),
not(C3_p = 9).

% The package with the computer in it is either the shipment that cost 6 or hayriye’s package.
% It only needs to take one option as a solution.
% C4_p is a dummy price for computer shipment.
% clue4(+H_i(Hayriye item),+Customers)
clue4(H_i,Customers):-
or([and([not(H_i = computer), (member([computer,_,C4_p], Customers), C4_p=6)]),
and([H_i = computer, (member([computer,_,C4_p], Customers), not(C4_p=6))])]).

% hayriye’s package cost 1 lira less than the shipment going to kadikoy.
% C5_p is a dummy price for kadikoy shipment.
% It uses arithmetic operation to see whether it achieves the condition.
% clue5(+H_p(Hayriye price),+Customers)
clue5(H_p,Customers):-
member([_,kadikoy,C5_p], Customers),
H_p - C5_p =:= -1.

%The shipment with the basketball in it is either naciye’s shipment or the package that cost 4.
% It only needs to take one option as a solution.
% C6_p is a dummy price for basketball shipment.
% clue6(+Nac_i(Naciye item),+Customers)
clue6(Nac_i,Customers):-
or([and([not(Nac_i = basketball), (member([basketball,_,C6_p],Customers), C6_p=4)]),
and([Nac_i = basketball, (member([basketball,_,C6_p], Customers), not(C6_p=4))])]).

% Neither the shipment with the rare book in it nor the package that cost 9 is feride’s shipment.
% clue7(+Fe_p(Feride price),+Fe_i(Feride item))
clue7(Fe_p,Fe_i):-
not(Fe_p= 9),
not(Fe_i = rare_book).

% The shipment going to uskudar is fatma’s.
% clue8(+Fa_t(Fatma town))
clue8(Fa_t):-
Fa_t =uskudar.

% The shipment that cost 8 is either feride’s shipment or nazan’s package.
% It only needs to take one option as a solution.
% clue9(+Naz_p(Nazan price),+Fe_p(Feride price))
clue9(Naz_p,Fe_p):-
or([and([not(Naz_p=8), Fe_p=8]), and([not(Fe_p=8), Naz_p=8])]).

% Of the package that cost 9 and ayse’s package, one contains the fruit basket and the other is going to beyoglu.
% Since it includes 'one contains' phrase for this form of information we can understand that left hand side cannot coincide within each other.
% Therefore, I also put a not condition.(This also applies for the clue11)
% C10_i and C10_t are dummy item and town for price 9 shipment.
% clue10(+A_p(Ayse price),+A_i(Ayse item),+A_t(Ayse town),+Customers)
clue10(A_p,A_i,A_t,Customers):-
member([C10_i, C10_t,9],Customers),
or([and([A_i = fruit_basket, C10_t = beyoglu]), and([A_t = beyoglu, C10_i = fruit_basket])]),
not(A_p=9).

% Of fatma’s package and the package going to besiktas, one cost 6 and the other contains the television.
% C11_i and C11_p are dummy item and price for besiktas shipment.
% clue11(+Fa_t(Fatma town),+Fa_i(Fatma item),+Fa_p(Fatma price),+Customers)
clue11(Fa_t,Fa_i,Fa_p,Customers):-
member([C11_i, besiktas,C11_p],Customers),
or([and([Fa_i = tv, C11_p = 6]), and([Fa_p = 6, C11_i = tv])]),
not(Fa_t=besiktas).