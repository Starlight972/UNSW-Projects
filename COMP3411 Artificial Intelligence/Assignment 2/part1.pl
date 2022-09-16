%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%       Assignment2 Part1       %%%%%%
%%%%%% 		Student Name: Xin Sun	 %%%%%%
%%%%%% 		    zID: z5248104		 %%%%%%
%%%%%%            22/04/2022         %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%====================================================
% QUESTION 1.1 List Processing 
%====================================================

% it is true if Number is even
even(Number) :- 0 is Number mod 2.

% it is true if Number is odd
odd(Number) :- 1 is Number mod 2.

% square the head with output in Res
square(Head, Res):-
    Res is Head * Head.

% Base case
% the result will be 0 if list is empty.
sumsq_even([],0).

% Head is even number case
sumsq_even([Head | Tail], Sum) :-
    even(Head),
    sumsq_even(Tail, RunningSum),
    square(Head, Res),
    Sum is Res + RunningSum.

% Head is odd number case
sumsq_even([Head | Tail], Sum) :-
    odd(Head),
    sumsq_even(Tail, Sum).


%====================================================
% QUESTION 1.2 Planning
%====================================================

clockwise_loc(mr, cs).
clockwise_loc(cs, off).
clockwise_loc(off, lab).
clockwise_loc(lab, mr).

counterclockwise_loc(off, cs).
counterclockwise_loc(cs, mr).
counterclockwise_loc(mr, lab).
counterclockwise_loc(lab, off).

% State of the robot's world = state(Robot Location, Robot Has Coffee, Sam Wants Coffee, Mail Waiting, Robot Has Mail)
% action(Action, State, NewState): Action in State produces NewState

action( mc,                                         %  move clockwise
        state(RLoc, RHC, SWC, MW, RHM),
        state(NextRLoc, RHC, SWC, MW, RHM)) :-
    clockwise_loc(RLoc, NextRLoc).

action( mcc,                                        %  move counterclockwise
        state(RLoc, RHC, SWC, MW, RHM),
        state(NextRLoc, RHC, SWC, MW, RHM)) :-
    counterclockwise_loc(RLoc, NextRLoc).

action( puc,                                        %  pickup coffee
        state(cs, false, SWC, MW, RHM),
        state(cs, true, SWC, MW, RHM)).

action( dc,                                         %  deliver coffee
        state(off, true, _, MW, RHM),
        state(off, false, false, MW, RHM)).

action( pum,                                        %  pickup mail
        state(mr, RHC, SWC, true, false),
        state(mr, RHC, SWC, false, true)).

action( pum,                                        %  deliver mail
        state(off, RHC, SWC, MW, true),
        state(off, RHC, SWC, MW, false)).

% plan(StartState, FinalState, Plan)

plan(State, State, []).                             % To achieve State from State itself, do nothing

plan(State1, GoalState, [Action1 | RestofPlan]) :-
    action(Action1, State1, State2),                % Make first action resulting in State2
    plan(State2, GoalState, RestofPlan).            % Find rest of plan

% Iterative deepening planner
% Backtracking to "append" generates lists of increasing length
% Forces "plan" to ceate fixed length plans

id_plan(Start, Goal, Plan) :-
    append(Plan, _, _),
    plan(Start, Goal, Plan).

% To test your action specifications, think about how you would ask the robot to pickup mail. What about if Sam want coffee and there was mail waiting?
% Ask the robot to pickup mail
% ?- id_plan(state(lab, false, false, true, false), state(_, _, _, false, _),Plan).
% Plan = [mc, pum] .

% Sam want coffee and there was mail waiting
% ?- id_plan(state(lab, false, true, true, false), state(_, _, false, false, _),Plan).
% Plan = [mc, pum, mc, puc, mc, dc] .

%====================================================
% QUESTION 1.3 Inductive Logic Programming
%====================================================

:- op(300, xfx, <-).

% Question 1.3 (a) Intra-construction
%----------------------------------------------------

intra_construction(C1 <- B1, C1 <- B2, C1 <- B3, C <- Z1B, C <- Z2B):-
    C1 == C1,
    intersection(B1, B2, B),
    gensym(z, C),
    subtract(B1, B, Z1B),
    subtract(B2, B, Z2B),
    append(B, [C], B3).


% Question 1.3 (b) Absorption
%----------------------------------------------------

absorption(C1 <- B1, C2 <- B2, C1 <- B1B, C2 <- B2):-
    C1 \= C2,
    subset(B2, B1),
    intersection(B1, B2, B),
    subtract(B1, B, X1),
    append([C2], X1, B1B).


% Question 1.3 (c) Truncation
%----------------------------------------------------

truncation(C1 <- B1, C1 <- B2, C1 <- B3) :-
    C1 == C1,
    intersection(B1, B2, B3).

