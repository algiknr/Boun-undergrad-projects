:-consult(algikanar_manualfacts).
:-consult(basicfacts).
% I explained the clues in algikanar_manualfacts.
% Expected time of the program between 15 and 25 seconds.

% memberperm eventually creates all possible different permutations of lists,then enables later calls to
% try changed versions of lists .
% memberperm(+[H],-List)
% memberperm(+[H|T],-List)
% member(?Elem, ?List)
memberperm([H],List) :- member(H,List).
memberperm([H|T],List) :- member(H,List), memberperm(T, List).

% allmembersetting lets memberperms to do the permutations for each section of the problem(item,town,price)
% in an ordered fashion.In the problemsolution part, each fail will be resulted in this area in a bottom up manner.
% It is not permutating customers since ,naturally, it's been chosen as a pivot for all the adressings.
% allmembersetting(+I(Itemlist),+T(Townlist),+P(Pricelist),-Alli(allitems),-Allt(alltowns),-Allp(allprices)).
allmembersetting(I,T,P,Alli,Allt,Allp):-

	memberperm(I, Alli),
    memberperm(T, Allt),
    memberperm(P, Allp).

% problemsolution takes the name of the customer and after applying the problem's clues writes the attained solution
% for the specific customer.
% problemsolution( +Name1)
problemsolution(Name1) :-

% The below four takes the list informations from basicfacts.
%(+I(Itemlist),+C(Customerlist),+T(Townlist),+P(Pricelist))
	item(I),
	customer(C),
	town(T),
	price(P),
    
% The below lists pack the information in order to permute them later on and ease evaluting the clues.	
% Unknown parameters of lists are named after the initials of the customer and the anticipated information.

    Ayse = [A_i,A_t,A_p],
    Fatma = [Fa_i,Fa_t,Fa_p],
	Hayriye = [H_i,H_t,H_p],
	Feride = [Fe_i,Fe_t,Fe_p],
	Nazan = [Naz_i,Naz_t,Naz_p],
	Naciye = [Nac_i,Nac_t,Nac_p],
	Alli = [A_i, Fa_i, H_i, Fe_i, Naz_i, Nac_i],
	Allt = [A_t, Fa_t, H_t, Fe_t, Naz_t, Nac_t],
	Allp = [A_p, Fa_p, H_p, Fe_p, Naz_p, Nac_p],
 
% This list holds the every other property for each customer. 
    Customers = [Ayse,Fatma,Hayriye,Feride,Nazan,Naciye],
	
% In each fail the lists will be reorganized. 
	allmembersetting(I,T,P,Alli,Allt,Allp),
	
% All clues arranged in a certain order since some of the clues are more obvious and easy to locate it is 
% better to put them in the first rows for a faster outcome. This situation can be used as an example to show 
% why this program is not a pure logic.The order of the values has an effect on deductions.
% From here onwards list informations will be tested according to clues and 
% it will whether redo with fails or exit and go on with the expected solution.
% It is basically looks for the answer of 'Does the list I have suit what I want?' until it is true. 

	% eighth rule
	clue8(Fa_t),
	
	% first rule
	clue1(H_t,Customers),
	
	% fifth rule
	clue5(H_p,Customers),
	
	% second rule
	clue2(Customers),
	
	% third rule
	clue3(Customers),
	
	% fourth rule
	clue4(H_i,Customers),
	
	% sixth rule
	clue6(Nac_i,Customers),
	
	% seventh rule
    clue7(Fe_p,Fe_i),
	
	% nineth rule
	clue9(Naz_p,Fe_p),
	
	% tenth rule
	clue10(A_p,A_i,A_t,Customers),
	
	% eleventh rule
	clue11(Fa_t,Fa_i,Fa_p,Customers),

% gives the names from customerlist
% nth0(?Index, ?List, ?Elem)	
	nth0(0,C,Ay),
	nth0(1,C,Fa),
	nth0(2,C,Ha),
	nth0(3,C,Fe),
	nth0(4,C,Naz),
	nth0(5,C,Nac),
	
% Since we are looking for a specific customer's information these lines condition the names and 
% write the output in a suitable format.
% write (+Term)
	(Name1==Ay->write('Shipment:'),write(ayse),write(','),write(A_i),write(','), write(A_t),write(','), write(A_p),write('.')
	; Name1==Fa->write('Shipment:'),write(fatma),write(','),write(Fa_i),write(','),write(Fa_t), write(','),write(Fa_p),write('.')
	; Name1==Ha->write('Shipment:'),write(hayriye),write(','),write(H_i),write(','),write(H_t),write(','),write(H_p),write('.')
	; Name1==Fe->write('Shipment:'),write(feride),write(','),write(Fe_i),write(','), write(Fe_t),write(','), write(Fe_p),write('.')
	; Name1==Naz->write('Shipment:'),write(nazan),write(','),write(Naz_i),write(','),write(Naz_t),write(','),write(Naz_p),write('.')
	; Name1==Nac->write('Shipment:'),write(naciye),write(','),write(Nac_i),write(','),write(Nac_t), write(','),write(Nac_p),write('.')
	;true),!.
	
%  This works as an indicator to start the problem solution and it is the calling of the program.
%  shipmentInfo(+Name1)	
shipmentInfo(Name1) :-
 
problemsolution(Name1).
