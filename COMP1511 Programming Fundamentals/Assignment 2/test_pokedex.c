// Assignment 2 19T3 COMP1511: Pokedex
// test_pokedex.c
//
// This file allows you to automatically test the functions you
// implement in pokedex.c.
//
// This program was written by Xin SUN (z5248104)
// on 24/11/2019
//
// Version 1.0.0: Assignment released.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "pokedex.h"

// Add your own #defines here.

// Sample data on Pikachu, the Pokemon with pokemon_id 25.
#define PIKACHU_ID 25
#define PIKACHU_NAME "Pikachu"
#define PIKACHU_HEIGHT 0.4
#define PIKACHU_WEIGHT 6.0
#define PIKACHU_FIRST_TYPE ELECTRIC_TYPE
#define PIKACHU_SECOND_TYPE NONE_TYPE

// Sample data on Rattata, the Pokemon with pokemon_id 19.
#define RATTATA_ID 19
#define RATTATA_NAME "Rattata"
#define RATTATA_HEIGHT 0.3
#define RATTATA_WEIGHT 3.5
#define RATTATA_FIRST_TYPE NORMAL_TYPE
#define RATTATA_SECOND_TYPE NONE_TYPE

// Sample data on Bulbasaur, the Pokemon with pokemon_id 1.
#define BULBASAUR_ID 1
#define BULBASAUR_NAME "Bulbasaur"
#define BULBASAUR_HEIGHT 0.7
#define BULBASAUR_WEIGHT 6.9
#define BULBASAUR_FIRST_TYPE GRASS_TYPE
#define BULBASAUR_SECOND_TYPE POISON_TYPE

// Sample data on Ivysaur, the Pokemon with pokemon_id 2.
#define IVYSAUR_ID 2
#define IVYSAUR_NAME "Ivysaur"
#define IVYSAUR_HEIGHT 1.0
#define IVYSAUR_WEIGHT 13.0
#define IVYSAUR_FIRST_TYPE GRASS_TYPE
#define IVYSAUR_SECOND_TYPE POISON_TYPE


// Add your own prototypes here.

// Tests for Stage 1
static void test_add_pokemon(void);
static void test_detail_pokemon(void);
static void test_find_current_pokemon(void);
static void test_print_pokemon(void);

// Tests for Stage 2
static void test_next_pokemon(void);
static void test_prev_pokemon(void);
static void test_change_current_pokemon(void);
static void test_remove_pokemon(void);

// Tests for Stage 3
// Test show_types
static void test_show_one_type_pokemon_types(void);
static void test_show_two_types_pokemon_types(void);
static void test_show_repeated_types(void);
static void test_show_empty_types(void);
// Test go_exploring
static void test_one_pokemon_go_explore(void);
static void test_different_types_go_explore(void);
static void test_same_type_go_explore(void);
static void test_mixed_types_go_explore(void);
static void test_empty_go_explore(void);
// Test count_total_pokemon
static void test_count_total_pokemon(void);
static void test_count_found_pokemon(void);


// Tests for Stage 4
// Test add evolution
static void test_add_pokemon_evolution(void);
// Test show evolution
static void test_show_evolution_all_found(void);
static void test_show_evolution_all_unfound(void);
static void test_show_evolution_mixed(void);
// Test get_next_revolution
static void test_get_next_evolution(void);
static void test_get_next_evolution_does_not_evolve(void);


// Tests for Pokedex functions from pokedex.c.
static void test_new_pokedex(void);
static void test_get_found_pokemon(void);


// Helper functions for creating/comparing Pokemon.
static Pokemon create_bulbasaur(void);
static Pokemon create_ivysaur(void);
static Pokemon create_pikachu(void);
static Pokemon create_rattata(void);
static int is_same_pokemon(Pokemon first, Pokemon second);
static int is_copied_pokemon(Pokemon first, Pokemon second);



int main(int argc, char *argv[]) {
    printf("Welcome to the COMP1511 Pokedex Tests!\n");

    printf("\n==================== Pokedex Tests ====================\n");
    // Tests for Stage 1
    test_add_pokemon();
    test_detail_pokemon();
    test_find_current_pokemon();
    test_print_pokemon();
    printf("\n==================== Passed Stage 1 ====================\n");

    // Tests for Stage 2
    test_next_pokemon();
    test_prev_pokemon();
    test_change_current_pokemon();
    test_remove_pokemon();
    printf("\n==================== Passed Stage 2 ====================\n");

    // Tests for Stage 3
    // Test show_types
    test_show_one_type_pokemon_types();
    test_show_two_types_pokemon_types();
    test_show_repeated_types();
    test_show_empty_types();
    // Test go_exploring
    test_one_pokemon_go_explore();
    test_different_types_go_explore();
    test_same_type_go_explore();
    test_mixed_types_go_explore();
    test_empty_go_explore();
    // Test count_total_pokemon
    test_count_total_pokemon();
    test_count_found_pokemon();
    printf("\n==================== Passed Stage 3 ====================\n");

    // Tests for Stage 4
    // Test add evolution
    test_add_pokemon_evolution();
    // Test show evolution
    test_show_evolution_all_found();
    test_show_evolution_all_unfound();
    test_show_evolution_mixed();
    // Test get_next_revolution
    test_get_next_evolution();
    test_get_next_evolution_does_not_evolve();
    printf("\n==================== Passed Stage 4 ====================\n");

    printf("\n==================== Congratulations!!! ====================\n");
    printf("\nAll Pokedex tests passed, you are Awesome!\n");
}


////////////////////////////////////////////////////////////////////////
//                     Pokedex Test Functions                         //
////////////////////////////////////////////////////////////////////////

// `test_new_pokedex` checks whether the new_pokedex and destroy_pokedex
// functions work correctly, to the extent that it can.
//
// It does this by creating a new Pokedex, checking that it's not NULL,
// then calling destroy_pokedex.
//
// Note that it isn't possible to check whether destroy_pokedex has
// successfully destroyed/freed the Pokedex, so the best we can do is to
// call the function and make sure that it doesn't crash..
static void test_new_pokedex(void) {
    printf("\n>> Testing new_pokedex\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("       --> Checking that the returned Pokedex is not NULL\n");
    assert(pokedex != NULL);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed new_pokedex tests!\n");
}




// `test_get_found_pokemon` checks whether the get_found_pokemon
// function works correctly.
//
// It does this by creating two Pokemon: Bulbasaur and Ivysaur (using
// the helper functions in this file and the provided code in pokemon.c).
//
// It then adds these to the Pokedex, sets Bulbasaur to be found, and
// then calls the get_found_pokemon function to get all of the Pokemon
// which have been found (which should be just the one, Bulbasaur).
//
// Some of the ways that you could extend these tests would include:
//   - calling the get_found_pokemon function on an empty Pokedex,
//   - calling the get_found_pokemon function on a Pokedex where none of
//     the Pokemon have been found,
//   - checking that the Pokemon in the new Pokedex are in ascending
//     order of pokemon_id (regardless of the order that they appeared
//     in the original Pokedex),
//   - checking that the currently selected Pokemon in the returned
//     Pokedex has been set correctly,
//   - checking that the original Pokedex has not been modified,
//   - ... and more!
static void test_get_found_pokemon(void) {
    printf("\n>> Testing get_found_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(get_current_pokemon(pokedex) == bulbasaur);
    
    printf("    ... Setting Bulbasaur to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Getting all found Pokemon\n");
    Pokedex found_pokedex = get_found_pokemon(pokedex);

    printf("       --> Checking the correct Pokemon were copied and returned\n");
    assert(count_total_pokemon(found_pokedex) == 1);
    assert(count_found_pokemon(found_pokedex) == 1);
    assert(is_copied_pokemon(get_current_pokemon(found_pokedex), bulbasaur));

    printf("    ... Destroying both Pokedexes\n");
    destroy_pokedex(pokedex);
    destroy_pokedex(found_pokedex);

    printf(">> Passed get_found_pokemon tests!\n");
}


// Write your own Pokedex tests here!

// Stage 1

// `test_add_pokemon` checks whether the add_pokemon function works
// correctly.
//
// It does this by creating the Pokemon Bulbasaur (using the helper
// functions in this file and the provided code in pokemon.c), and
// calling add_pokemon to add it to the Pokedex.
//
// Some of the ways that you could extend these test would include:
//   - adding additional Pokemon other than just Bulbasaur,
//   - checking whether the currently selected Pokemon is correctly set,
//   - checking that functions such as `count_total_pokemon` return the
//     correct result after more Pokemon are added,
//   - ... and more!
static void test_add_pokemon(void) {
    printf("\n>> Testing add_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed add_pokemon tests!\n");
}

static void test_detail_pokemon(void) {
    printf("\n>> Testing detail_pookemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();
    
    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    
    printf("    ... Showing details of the Pokemon\n");
    detail_pokemon(pokedex);
    
    printf("    ... Letting the Pokemon be found\n");
    find_current_pokemon(pokedex);
    
    printf("    ... Showing details of the Pokemon\n");
    detail_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed detail_pokemon tests!\n");
}

static void test_find_current_pokemon(void) {
    printf("\n>> Testing find_current_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();
    
    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Letting the Pokemon be found\n");
    find_current_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed find_current_pokemon tests!\n");
}

static void test_print_pokemon(void) {
    printf("\n>> Testing print_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Showing the Pokemons in the Pokedex\n");
    print_pokemon(pokedex);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed next_pokemon tests!\n");
}

// Stage 2

// `test_next_pokemon` checks whether the next_pokemon function works
// correctly.
//
// It does this by creating two Pokemon: Bulbasaur and Ivysaur (using
// the helper functions in this file and the provided code in pokemon.c).
//
// It then adds these to the Pokedex, then checks that calling the
// next_pokemon function changes the currently selected Pokemon from
// Bulbasaur to Ivysaur.
//
// Some of the ways that you could extend these tests would include:
//   - adding even more Pokemon to the Pokedex,
//   - calling the next_pokemon function when there is no "next" Pokemon,
//   - calling the next_pokemon function when there are no Pokemon in
//     the Pokedex,
//   - ... and more!
static void test_next_pokemon(void) {
    printf("\n>> Testing next_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next pokemon\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed next_pokemon tests!\n");
}

static void test_prev_pokemon(void) {
    printf("\n>> Testing prev_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);

    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next pokemon\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Moving to the previous pokemon\n");
    prev_pokemon(pokedex);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);

    printf(">> Passed prev_pokemon tests!\n");
}

static void test_change_current_pokemon(void) {
    printf("\n>> Testing change_current_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Move to next pokemon\n");
    next_pokemon(pokedex);
    
    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Moving to pokemon with ID 1\n");
    change_current_pokemon(pokedex, 1);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed change_current_pokemon test!\n");
}

static void test_remove_pokemon(void) {
    printf("\n>> Testing remove_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Pikachu\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon pikachu = create_pikachu();

    printf("    ... Adding Bulbasaur, Ivysaur and Pikachu to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, pikachu);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Move to next pokemon\n");
    next_pokemon(pokedex);
    
    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Move to next pokemon\n");
    next_pokemon(pokedex);
    
    printf("       --> Checking that the current Pokemon is Pikachu\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), pikachu));
    
    printf("    ... Moving to pokemon with ID 2\n");
    change_current_pokemon(pokedex, 2);
    
    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Removing the current pokemon\n");
    remove_pokemon(pokedex);
    
    printf("       --> Checking that the current Pokemon is Pikachu\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), pikachu));
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed remove_pokemon test!\n");
}

// Stage 3

// Test show_types
static void test_show_one_type_pokemon_types(void) {
    printf("\n>> Testing show_one_type_pokemon_types\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Pikachu and Rattata\n");
    Pokemon pikachu = create_pikachu();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Pikachu and Rattata to the Pokedex\n");
    add_pokemon(pokedex, pikachu);
    add_pokemon(pokedex, rattata);
    
    printf("    ... Showing types\n");
    show_types(pokedex);
    
    printf("    ... Showing reference\n");
    printf("Electric\nNormal\n");
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_one_type_pokemon_types test!\n");
}
// Test show types of pokemons with two types
static void test_show_two_types_pokemon_types(void) {
    printf("\n>> Testing show_two_types_pokemon_types\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, rattata);
    
    printf("    ... Showing types\n");
    show_types(pokedex);
    
    printf("    ... Showing reference\n");
    printf("Poison\nGrass\nNormal\n");
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_two_types_pokemon_types test!\n");
}

// Test show types of pokemos with the same type
static void test_show_repeated_types(void) {
    printf("\n>> Testing show_repeated_pokemon_types\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    
    printf("    ... Showing types\n");
    show_types(pokedex);
    
    printf("    ... Showing reference\n");
    printf("Poison\nGrass\n");
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_repeated_types test!\n");
}

// Test show types of an empty pokedex
static void test_show_empty_types(void) {
    printf("\n>> Testing show_empty_types\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();
    
    printf("    ... Showing types\n");
    show_types(pokedex);
    
    printf("    ... Showing reference\n");
    printf("\n(There should be nothing)\n");
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_empty_types test!\n");
}

// Test go_exploring
static void test_one_pokemon_go_explore(void) {
    printf("\n>> Testing one_pokemon_go_explore\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur\n");
    Pokemon bulbasaur = create_bulbasaur();

    printf("    ... Adding Bulbasaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Showing the detail of the pokemon\n");
    detail_pokemon(pokedex);

    printf("    ... Printing reference detail of Bulbasaur\n");
    printf("ID: 001\nName: *********\nHeight: --\nWeight: --\nType: --\n");

    printf("    ... Go exploring\n");
    go_exploring(pokedex);
    
    printf("    ... Showing the detail of current pokemon\n");
    detail_pokemon(pokedex);

    printf("    ... Printing reference detail of Bulbasaur\n");
    printf("ID: 001\nName: Balbasaur\nHeight: 0.7m\nWeight: 6.9kg\nType: Fire Poison\n");
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed one_pokemon_go_explore test!\n");
}
// Test go exploring when the pokemons in the list are of different types
static void test_different_types_go_explore(void) {
    printf("\n>> Testing different_types_go_explore\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Pikachu\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon pikachu = create_pikachu();

    printf("    ... Adding Bulbasaur and Pikachu to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, pikachu);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Pikachu\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), pikachu));
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);

    printf("    ... Go exploring\n");
    go_exploring(pokedex);
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed different_types_go_explore test!\n");
}

// Test go exploring when some of the same type
static void test_same_type_go_explore(void) {
    printf("\n>> Testing same_type_go_explore\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur and Ivysaur\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();

    printf("    ... Adding Bulbasaur and Ivysaur to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);

    printf("    ... Go exploring\n");
    go_exploring(pokedex);
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed same_type_go_explore test!\n");
}

static void test_mixed_types_go_explore(void) {
    printf("\n>> Testing mixed_types_go_explore\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Pikachu\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon pikachu = create_pikachu();

    printf("    ... Adding Bulbasaur, Ivysaur and Pikachu to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, pikachu);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Pikachu\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), pikachu));
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);

    printf("    ... Go exploring\n");
    go_exploring(pokedex);
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed mixed_types_go_explore test!\n");
}

// Test go exploring on an empty pokedex
static void test_empty_go_explore(void) {
    printf("\n>> Testing empty_pokedex_go_explore\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);

    printf("    ... Go exploring\n");
    go_exploring(pokedex);
    
    printf("    ... Showing the list of pokemon\n");
    print_pokemon(pokedex);
    
    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed empty_go_explore test!\n");
}

static void test_count_total_pokemon(void) {
    printf("\n>> Testing count_total_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("       --> Checking that total pokemon is 3\n");
    assert(count_total_pokemon(pokedex) == 3);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed count_total_pokemon test!\n");
}

static void test_count_found_pokemon(void) {
    printf("\n>> Testing count_found_pokemon\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("       --> Checking that found pokemon is 2\n");
    assert(count_found_pokemon(pokedex) == 2);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed count_found_pokemon test!\n");
}

// Stage 4

static void test_add_pokemon_evolution(void) {
    printf("\n>> Testing add_pokemon_evolution\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Pikachu\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Setting evolve 1 to 19\n");
    add_pokemon_evolution(pokedex, 1, 19);
    
    printf("    ... Setting evolve 19 to 2\n");
    add_pokemon_evolution(pokedex, 19, 2);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed add_pokemon_evolution test!\n");
}

// Test show evolution
static void test_show_evolution_all_found(void) {
    printf("\n>> Testing show_evolution_all_found\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);
    
    printf("    ... Changing the current pokemon to be ID 1\n");
    change_current_pokemon(pokedex, 1);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison]\n");
    
    printf("    ... Setting evolve 1 to 19\n");
    add_pokemon_evolution(pokedex, 1, 19);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison] --> #019 Rattata [Normal]\n");
    
    printf("    ... Setting evolve 19 to 2\n");
    add_pokemon_evolution(pokedex, 19, 2);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison] --> #019 Rattata [Normal] --> #002 Ivysaur [Grass, Poison]\n");

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_evolution_all_found test!\n");
}

// Test show evolution all pokemon unfound
static void test_show_evolution_all_unfound(void) {
    printf("\n>> Testing show_evolution_all_unfound\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Changing the current pokemon to be ID 1\n");
    change_current_pokemon(pokedex, 1);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 ???? [????]\n");
    
    printf("    ... Setting evolve 1 to 19\n");
    add_pokemon_evolution(pokedex, 1, 19);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 ???? [????] --> #019 ???? [????]\n");
    
    printf("    ... Setting evolve 19 to 2\n");
    add_pokemon_evolution(pokedex, 19, 2);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 ???? [????] --> #019 ???? [????] --> #002 ???? [????]\n");

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_evolution_all_unfound test!\n");
}

// Test show evolution of pokemons mixed found and not found
static void test_show_evolution_mixed(void) {
    printf("\n>> Testing show_evolution_mixed\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Changing the current pokemon to be ID 1\n");
    change_current_pokemon(pokedex, 1);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison]\n");
    
    printf("    ... Setting evolve 1 to 19\n");
    add_pokemon_evolution(pokedex, 1, 19);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison] --> #019 ???? [????]\n");
    
    printf("    ... Setting evolve 19 to 2\n");
    add_pokemon_evolution(pokedex, 19, 2);
    
    printf("    ... Showing the revolution of current pokemon\n");
    show_evolutions(pokedex);
    
    printf("    ... Printing the expected result\n");
    printf("#001 Bulbasaur [Grass, Poison] --> #019 ???? [????] --> #002 Ivysaur [Grass, Poison]\n");

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed show_evolution_mixed test!\n");
}

static void test_get_next_evolution(void) {
    printf("\n>> Testing get_next_evolution\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Changing the current pokemon to be ID 1\n");
    change_current_pokemon(pokedex, 1);
    
    printf("    ... Setting evolve 1 to 125\n");
    add_pokemon_evolution(pokedex, 1, 125);
    
    printf("    --> Checking the ID the current Pokemon evolve in is 125\n");
    assert(get_next_evolution(pokedex) == 125);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed get_next_evolution test!\n");
}

// Test get next evolution when it doesn't evolve
static void test_get_next_evolution_does_not_evolve(void) {
    printf("\n>> Testing get_next_evolution_does_not_evolve\n");

    printf("    ... Creating a new Pokedex\n");
    Pokedex pokedex = new_pokedex();

    printf("    ... Creating Bulbasaur, Ivysaur and Rattata\n");
    Pokemon bulbasaur = create_bulbasaur();
    Pokemon ivysaur = create_ivysaur();
    Pokemon rattata = create_rattata();

    printf("    ... Adding Bulbasaur, Ivysaur and Rattata to the Pokedex\n");
    add_pokemon(pokedex, bulbasaur);
    add_pokemon(pokedex, ivysaur);
    add_pokemon(pokedex, rattata);
    
    printf("       --> Checking that the current Pokemon is Bulbasaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), bulbasaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Ivysaur\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), ivysaur));
    
    printf("    ... Setting the current pokemon to be found\n");
    find_current_pokemon(pokedex);

    printf("    ... Moving to the next\n");
    next_pokemon(pokedex);

    printf("       --> Checking that the current Pokemon is Rattata\n");
    assert(is_same_pokemon(get_current_pokemon(pokedex), rattata));
    
    printf("    ... Changing the current pokemon to be ID 2\n");
    change_current_pokemon(pokedex, 2);
    
    printf("    ... Setting evolve 1 to 19\n");
    add_pokemon_evolution(pokedex, 1, 19);
    
    printf("    --> Checking the current pokemon does not evolve\n");
    assert(get_next_evolution(pokedex) == DOES_NOT_EVOLVE);

    printf("    ... Destroying the Pokedex\n");
    destroy_pokedex(pokedex);
    
    printf(">> Passed get_next_evolution_does_not_evolve test!\n");
}



////////////////////////////////////////////////////////////////////////
//                     Helper Functions                               //
////////////////////////////////////////////////////////////////////////

// Helper function to create Bulbasaur for testing purposes.
static Pokemon create_bulbasaur(void) {
    Pokemon pokemon = new_pokemon(
            BULBASAUR_ID, BULBASAUR_NAME,
            BULBASAUR_HEIGHT, BULBASAUR_WEIGHT,
            BULBASAUR_FIRST_TYPE,
            BULBASAUR_SECOND_TYPE
    );
    return pokemon;
}

// Helper function to create Ivysaur for testing purposes.
static Pokemon create_ivysaur(void) {
    Pokemon pokemon = new_pokemon(
            IVYSAUR_ID, IVYSAUR_NAME,
            IVYSAUR_HEIGHT, IVYSAUR_WEIGHT,
            IVYSAUR_FIRST_TYPE,
            IVYSAUR_SECOND_TYPE
    );
    return pokemon;
}




// Helper function to compare whether two Pokemon are the same.
// This checks that the two pointers contain the same address, i.e.
// they are both pointing to the same pokemon struct in memory.
//
// Pokemon ivysaur = new_pokemon(0, 'ivysaur', 1.0, 13.0, GRASS_TYPE, POISON_TYPE)
// Pokemon also_ivysaur = ivysaur
// is_same_pokemon(ivysaur, also_ivysaur) == TRUE
static int is_same_pokemon(Pokemon first, Pokemon second) {
    return first == second;
}

// Helper function to compare whether one Pokemon is a *copy* of
// another, based on whether their attributes match (e.g. pokemon_id,
// height, weight, etc).
// 
// It also checks that the pointers do *not* match -- i.e. that the
// pointers aren't both pointing to the same pokemon struct in memory.
// If the pointers both contain the same address, then the second
// Pokemon is not a *copy* of the first Pokemon.
// 
// This function doesn't (yet) check that the Pokemon's names match
// (but perhaps you could add that check yourself...).
static int is_copied_pokemon(Pokemon first, Pokemon second) {
    return (pokemon_id(first) == pokemon_id(second))
    &&  (first != second)
    &&  (pokemon_height(first) == pokemon_height(second))
    &&  (pokemon_weight(first) == pokemon_weight(second))
    &&  (pokemon_first_type(first) == pokemon_first_type(second))
    &&  (pokemon_second_type(first) == pokemon_second_type(second));
}

// Write your own helper functions here!
// Helper function to creat Pikachu for testing purposes
static Pokemon create_pikachu(void) {
    Pokemon pokemon = new_pokemon(
            PIKACHU_ID, PIKACHU_NAME,
            PIKACHU_HEIGHT, PIKACHU_WEIGHT,
            PIKACHU_FIRST_TYPE,
            PIKACHU_SECOND_TYPE
    );
    return pokemon;
}

// Helper function to creat Rattata for testing purposes
static Pokemon create_rattata(void) {
    Pokemon pokemon = new_pokemon(
            RATTATA_ID, RATTATA_NAME,
            RATTATA_HEIGHT, RATTATA_WEIGHT,
            RATTATA_FIRST_TYPE,
            RATTATA_SECOND_TYPE
    );
    return pokemon;
}


