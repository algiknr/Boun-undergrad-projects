
location(T1,R,C) :-
  T0  is T1 - 1,
  RN  is R - 1,
  RS  is R + 1,
  CW  is C - 1,
  CE  is C + 1,
  (
    ((action(T0,eat);action(T0,clockWise);action(T0,counterClockWise)), location(T0,R,C));
    ((action(T0,attack);action(T0,forward)), bump(T1), location(T0,R,C));
    ((action(T0,attack);action(T0,forward)), dir(T0,north), not(bump(T1)), location(T0,RS,C));
    ((action(T0,attack);action(T0,forward)), dir(T0,south), not(bump(T1)), location(T0,RN,C));
    ((action(T0,attack);action(T0,forward)), dir(T0,west),  not(bump(T1)), location(T0,R,CE));
    ((action(T0,attack);action(T0,forward)), dir(T0,east),  not(bump(T1)), location(T0,R,CW))
  ).
  
dir(T1,north) :-
  T0 is T1 - 1,
		(
				((action(T0,eat);action(T0,attack);action(T0,forward)), dir(T0,north) );
				(action(T0,clockWise)       , dir(T0,west));
				(action(T0,counterClockWise), dir(T0,east))
		).

dir(T1,east) :-
  T0 is T1 - 1,
		(
				((action(T0,eat);action(T0,attack);action(T0,forward)), dir(T0,east));
				(action(T0,clockWise)       , dir(T0,north));
				(action(T0,counterClockWise), dir(T0,south))
		).

dir(T1,south) :-
  T0 is T1 - 1,
		(
				((action(T0,eat);action(T0,attack);action(T0,forward)), dir(T0,south));
				(action(T0,clockWise)       , dir(T0,east));
				(action(T0,counterClockWise), dir(T0,west))
		).

dir(T1,west) :-
  T0 is T1 - 1,
		(
				((action(T0,eat);action(T0,attack);action(T0,forward)), dir(T0,west) );
				(action(T0,clockWise)       , dir(T0,south));
				(action(T0,counterClockWise), dir(T0,north))
		).

  
  
bumploc(T1,R,C) :-
  T0  is T1 - 1,
  RN  is R - 1,
  RS  is R + 1,
  CW  is C - 1,
  CE  is C + 1,
  
  (
    ((action(T0,attack);action(T0,forward)), bump(T1),
	(
	(location(T0,RN,C),dir(T0,south));
	(location(T0,R,CW),dir(T0,east));
	(location(T0,RS,C),dir(T0,north));
	(location(T0,R,CE),dir(T0,west))
	))
  
  ).
  
  
   
eatloc(T1,R,C) :-

	action(T1,eat),location(T1,R,C). 
   
    
   
attackloc(T1,R,C) :-
  RN  is R - 1,
  RS  is R + 1,
  CW  is C - 1,
  CE  is C + 1,
  
  (
    (action(T1,attack),
	(
	(location(T1,RN,C),dir(T1,south));
	(location(T1,R,CW),dir(T1,east));
	(location(T1,RS,C),dir(T1,north));
	(location(T1,R,CE),dir(T1,west))
	))
  
  ).
  
 
controlsouthwumpus(S,X,Y,D):-(
	 (D==south,findWumpusSmell(WumpusSmellList),
	 findall( [T1], ( member(T1, WumpusSmellList),((RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).
	 
controlnorthwumpus(S,X,Y,D):-(
	 (D==north,findWumpusSmell(WumpusSmellList),
	 findall( [T1], ( member(T1, WumpusSmellList),((RN is X-1,location(T1,RN,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).	

controleastwumpus(S,X,Y,D):-(
	 (D==east,findWumpusSmell(WumpusSmellList),
	 findall( [T1], ( member(T1, WumpusSmellList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CE))))
	 
	 ).	

controlwestwumpus(S,X,Y,D):-(
	 (D==west,findWumpusSmell(WumpusSmellList),
	 findall( [T1], ( member(T1, WumpusSmellList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CW is Y-1,(hasBeenThere(S,RS,Y);hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW))))
	 
	 ).	
	 
controlsouthbreeze(S,X,Y,D):-(
	 (D==south,findWhenBreeze(BreezeList),
	 findall( [T1], ( member(T1, BreezeList),((RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).
	 
controlnorthbreeze(S,X,Y,D):-(
	 (D==north,findWhenBreeze(BreezeList),
	 findall( [T1], ( member(T1, BreezeList),((RN is X-1,location(T1,RN,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).	

controleastbreeze(S,X,Y,D):-(
	 (D==east,findWhenBreeze(BreezeList),
	 findall( [T1], ( member(T1, BreezeList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CE))))
	 
	 ).	

controlwestbreeze(S,X,Y,D):-(
	 (D==west,findWhenBreeze(BreezeList),
	 findall( [T1], ( member(T1, BreezeList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CW is Y-1,(hasBeenThere(S,RS,Y);hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW))))
	 
	 ).		

controlsouthfood(S,X,Y,D):-(
	 (D==south,findFoodSmell(FoodSmellList),
	 findall( [T1], ( member(T1, FoodSmellList),((RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).
	 
controlnorthfood(S,X,Y,D):-(
	 (D==north,findFoodSmell(FoodSmellList),
	 findall( [T1], ( member(T1, FoodSmellList),((RN is X-1,location(T1,RN,Y));(CW is Y-1,location(T1,X,CW));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE))))
	 
	 ).	

controleastfood(S,X,Y,D):-(
	 (D==east,findFoodSmell(FoodSmellList),
	 findall( [T1], ( member(T1, FoodSmellList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CE is Y+1,location(T1,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CE))))
	 
	 ).	

controlwestfood(S,X,Y,D):-(
	 (D==west,findFoodSmell(FoodSmellList),
	 findall( [T1], ( member(T1, FoodSmellList),((RN is X-1,location(T1,RN,Y));(RS is X+1,location(T1,RS,Y));(CW is Y-1,location(T1,X,CW)))),Intersect1),	 
	 (is_empty(Intersect1)),(RN is X-1,RS is X+1,CW is Y-1,(hasBeenThere(S,RS,Y);hasBeenThere(S,RN,Y);hasBeenThere(S,X,CW))))
	 
	 ).	 
	 
hasFoodSense(T,X,Y):- ( 
	not(hasNotFoodSense(T,X,Y)),
	RN is X-1,
	RS is X+1,
	CW is Y-1,
	CE is Y+1,
	
	(
	
	((RNN is RN-1,(hasBeenThere(T,RNN,Y);controlnorthfood(T,RNN,Y,north);isWall(T,RNN,Y);(RNN=:=0))),
	((hasBeenThere(T,RN,CW);controlwestfood(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastfood(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	((RSS is RS+1,(hasBeenThere(T,RSS,Y);controlsouthfood(T,RSS,Y,south);isWall(T,RSS,Y);(RSS=:=0))),
	((hasBeenThere(T,RN,CW);controlwestfood(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastfood(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	(((hasBeenThere(T,RN,CW);controlnorthfood(T,RN,CW,north);isWall(T,RN,CW);(RN=:=0))),
	(CWW is CW-1,(hasBeenThere(T,X,CWW);controlwestfood(T,X,CWW,west);isWall(T,X,CWW);(CWW=:=0))),
	((hasBeenThere(T,RS,CW);controlsouthfood(T,RS,CW,south);isWall(T,RS,CW);(RS=:=0))));
	
	(((hasBeenThere(T,RN,CE);controlnorthfood(T,RN,CE,north);isWall(T,RN,CE);(RN=:=0))),
	(CEE is CE+1,(hasBeenThere(T,X,CEE);controleastfood(T,X,CEE,east);isWall(T,X,CEE);(CEE=:=0))),
	((hasBeenThere(T,RS,CE);controlsouthfood(T,RS,CE,south);isWall(T,RS,CW);(RS=:=0))))
	)
	
	).
	
hasNotFoodSense(S,X,Y):-
     (findFoodSmell(FoodSmellList),
	 findall( [T], ( member(T, FoodSmellList),((RN is X-1,location(T,RN,Y));(RS is X+1,location(T,RS,Y));(CW is Y-1,location(T,X,CW));(CE is Y+1,location(T,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),
	 (RN is X-1,RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE)))).
	 


		
hasBeenThere(T,X,Y):-( 
	findTime(ActionTimes),list_to_set(ActionTimes,LS),findall([T2], ( member(T2, LS),location(T2,X,Y)),Intersect2),
	not(is_empty(Intersect2))).
		
		
findWhenBumped(BumpedTimeList) :- findall(T_prime ,(bump(T), T_prime is T),BumpedTimeList).

findWhenAttack(AttackTimeList) :- findall(T_prime ,(action(T,attack), T_prime is T),AttackTimeList).

findWhenEat(EatTimeList) :- findall(T_prime ,(action(T,eat), T_prime is T),EatTimeList).

findWhenBreeze(BreezeList) :- findall(T_prime ,(pitBreeze(T), T_prime is T ),BreezeList).

findWumpusSmell(WumpusSmellList) :- findall(T_prime ,(wumpusSmell(T), T_prime is T ),WumpusSmellList).

findFoodSmell(FoodSmellList) :- findall(T_prime ,(foodSmell(T), T_prime is T ),FoodSmellList).

findTime(ActionTimes):-findall(T_prime ,(
(action(T,forward);action(T,counterClockWise);action(T,clockWise);action(T,attack);action(T,eat);bump(T);wumpusSmell(T);foodSmell(T);pitBreeze(T);full(T)), T_prime is T ),ActionTimes).



isWall(T,R,C):- 
    isWall(R,C).
	
is_empty(List):- not(member(_,List)).	

isWall(X,Y):- 
       
        (X =:= 0;
         Y =:= 0);
        (
	 findWhenBumped(BumpedTimeList),
	 findall( [T], ( member(T, BumpedTimeList),bumploc(T, X, Y) ), BumpedRes),
	 not(is_empty(BumpedRes))
        ).		

isClear(T,R,C) :-     
    hasNotWumpus(T,R,C),
    hasNotPit(T,R,C),
    not(isWall(R,C)).

hasNotWumpus(S,X,Y):-
	 (findWumpusSmell(WumpusSmellList),
	 findall( [T], ( member(T, WumpusSmellList),((RN is X-1,location(T,RN,Y));(RS is X+1,location(T,RS,Y));(CW is Y-1,location(T,X,CW));(CE is Y+1,location(T,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),
	 (RN is X-1,RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE)))).	

hasNotPit(S,X,Y):-
     (findWhenBreeze(BreezeList),
	 findall( [T], ( member(T, BreezeList),((RN is X-1,location(T,RN,Y));(RS is X+1,location(T,RS,Y));(CW is Y-1,location(T,X,CW));(CE is Y+1,location(T,X,CE)))),Intersect1),	 
	 (is_empty(Intersect1)),
	 (RN is X-1,RS is X+1,CW is Y-1,CE is Y+1,(hasBeenThere(S,RN,Y);hasBeenThere(S,RS,Y);hasBeenThere(S,X,CW);hasBeenThere(S,X,CE)))).			
		
	
hasPit(T,X,Y):- ( 

	not(hasNotPit(T,X,Y)),
	RN is X-1,
	RS is X+1,
	CW is Y-1,
	CE is Y+1,
	
	(
	
	((RNN is RN-1,(hasBeenThere(T,RNN,Y);controlnorthbreeze(T,RNN,Y,north);isWall(T,RNN,Y);(RNN=:=0))),
	((hasBeenThere(T,RN,CW);controlwestbreeze(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastbreeze(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	((RSS is RS+1,(hasBeenThere(T,RSS,Y);controlsouthbreeze(T,RSS,Y,south);isWall(T,RSS,Y);(RSS=:=0))),
	((hasBeenThere(T,RN,CW);controlwestbreeze(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastbreeze(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	(((hasBeenThere(T,RN,CW);controlnorthbreeze(T,RN,CW,north);isWall(T,RN,CW);(RN=:=0))),
	(CWW is CW-1,(hasBeenThere(T,X,CWW);controlwestbreeze(T,X,CWW,west);isWall(T,X,CWW);(CWW=:=0))),
	((hasBeenThere(T,RS,CW);controlsouthbreeze(T,RS,CW,south);isWall(T,RS,CW);(RS=:=0))));
	
	(((hasBeenThere(T,RN,CE);controlnorthbreeze(T,RN,CE,north);isWall(T,RN,CE);(RN=:=0))),
	(CEE is CE+1,(hasBeenThere(T,X,CEE);controleastbreeze(T,X,CEE,east);isWall(T,X,CEE);(CEE=:=0))),
	((hasBeenThere(T,RS,CE);controlsouthbreeze(T,RS,CE,south);isWall(T,RS,CW);(RS=:=0))))
	)
	
	).
	
hasWumpus(T,X,Y):- ( 
	not(hasNotWumpus(T,X,Y)),
	RN is X-1,
	RS is X+1,
	CW is Y-1,
	CE is Y+1,
	
	(
	
	((RNN is RN-1,(hasBeenThere(T,RNN,Y);controlnorthwumpus(T,RNN,Y,north);isWall(T,RNN,Y);(RNN=:=0))),
	((hasBeenThere(T,RN,CW);controlwestwumpus(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastwumpus(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	((RSS is RS+1,(hasBeenThere(T,RSS,Y);controlsouthwumpus(T,RSS,Y,south);isWall(T,RSS,Y);(RSS=:=0))),
	((hasBeenThere(T,RN,CW);controlwestwumpus(T,RN,CW,west);isWall(T,RN,CW);(CW=:=0))),
	((hasBeenThere(T,RN,CE);controleastwumpus(T,RN,CE,east);isWall(T,RN,CE);(CE=:=0))));
	
	(((hasBeenThere(T,RN,CW);controlnorthwumpus(T,RN,CW,north);isWall(T,RN,CW);(RN=:=0))),
	(CWW is CW-1,(hasBeenThere(T,X,CWW);controlwestwumpus(T,X,CWW,west);isWall(T,X,CWW);(CWW=:=0))),
	((hasBeenThere(T,RS,CW);controlsouthwumpus(T,RS,CW,south);isWall(T,RS,CW);(RS=:=0))));
	
	(((hasBeenThere(T,RN,CE);controlnorthwumpus(T,RN,CE,north);isWall(T,RN,CE);(RN=:=0))),
	(CEE is CE+1,(hasBeenThere(T,X,CEE);controleastwumpus(T,X,CEE,east);isWall(T,X,CEE);(CEE=:=0))),
	((hasBeenThere(T,RS,CE);controlsouthwumpus(T,RS,CE,south);isWall(T,RS,CW);(RS=:=0))))
	)
	
	).

hasDeadWumpus(S,X,Y):-
    (
	 findWhenAttack(AttackTimeList),
	 findall( [T], ( member(T, AttackTimeList),attackloc(T, X, Y) ), AttackRes),
	 not(is_empty(AttackRes))
        ).
		

hasFood(S,X,Y):-
	 findWhenEat(EatTimeList),
	 findall( [T], ( member(T, EatTimeList),eatloc(T, X, Y) ), EatRes),
	 (not(is_empty(EatRes))->(findall( [T], ( member(T, EatRes),S<T),FinalEatRes),not(is_empty(FinalEatRes)));(hasFoodSense(S,X,Y))).
	 
hasNotFood(S,X,Y):-
	 findWhenEat(EatTimeList),
	 findall( [T], ( member(T, EatTimeList),eatloc(T, X, Y) ), EatRes),
	 (not(is_empty(EatRes))->(findall( [T], ( member(T, EatRes),not(S<T)),FinalEatRes),not(is_empty(FinalEatRes)));(hasNotFoodSense(S,X,Y))).
	 	 




isWall(-10,-10).
isWall(-10,-10,-10).

bump(-10).
wumpusSmell(-10).
foodSmell(-10).
pitBreeze(-10).
action(-10,blanc).
full(-10).

