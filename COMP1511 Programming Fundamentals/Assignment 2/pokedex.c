// Assignment 2 19T3 COMP1511: Pokedex
// pokedex.c
//
// This program was written by Xin SUN (z5248104)
// on 17/11/2019
//
// Version 2.0.0: Release

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// Note you are not allowed to use <string.h> in this assignment
// There are some techniques we would like you to learn to code
// that the string library trivialises.

// ----------------------------------------------
// Add any extra #includes your code needs here.
// ----------------------------------------------

#include "pokedex.h"


// ----------------------------------------------
// Add your own #defines here.
// ----------------------------------------------


// Note you are not permitted to use arrays in struct pokedex,
// you must use a linked list.
//
// The only exception is that char arrays are permitted for
// search_pokemon and functions it may call, as well as the string
// returned by pokemon_name (from pokemon.h).
//
// You will need to add fields to struct pokedex.
// You may change or delete the head field.
struct pokedex {
    struct pokenode *head;
    struct pokenode *cur_pokemon;

};


// You don't have to use the provided struct pokenode, you are free to
// make your own struct instead.
//
// If you use the provided struct pokenode, you will need to add fields
// to it to store other information.
struct pokenode {
    Pokemon pokemon;
    struct pokenode *next;
    struct pokenode *previous;
    int found;
    int evolve_id;
};


// ----------------------------------------------
// Add your own structs here.
// ----------------------------------------------




// ----------------------------------------------
// Add prototypes for your own functions here.
// ----------------------------------------------
int is_new_type(pokemon_type type, Pokedex typedex);

// Creates a new pokenode struct and returns a pointer to it.
static struct pokenode *new_pokenode(Pokemon pokemon);



// You need to implement the following functions in their stages.
// In other words, replace the lines calling fprintf & exit with your code.
// You can find descriptions of what each function should do in pokedex.h


// Creates a new Pokedex, and returns a pointer to it.
// Note: you will need to modify this function.
Pokedex new_pokedex(void) {
    // Malloc memory for a new Pokedex, and check that the memory
    // allocation succeeded.
    Pokedex pokedex = malloc(sizeof(struct pokedex));
    assert(pokedex != NULL);
    // Set the head of the linked list to be NULL.
    // (i.e. set the Pokedex to be empty)
    pokedex->head = NULL;
    // TODO: Add your own code here.
    pokedex->cur_pokemon = NULL;
    return pokedex;
}

// Create a new pokenode struct and returns a pointer to it.
//
// This function should allocate memory for a pokenode, set its pokemon
// pointer to point to the specified pokemon, and return a pointer to
// the allocated memory.
static struct pokenode *new_pokenode(Pokemon pokemon) {
    struct pokenode *new_pokenode = malloc (sizeof(struct pokenode));
    new_pokenode->pokemon = pokemon;
    new_pokenode->next = NULL;
    new_pokenode->previous = NULL;
    new_pokenode->found = 0;
    new_pokenode->evolve_id = DOES_NOT_EVOLVE;
    return new_pokenode;
}

//////////////////////////////////////////////////////////////////////
//                         Stage 1 Functions                        //
//////////////////////////////////////////////////////////////////////

// Add a new Pokemon to the Pokedex.
void add_pokemon(Pokedex pokedex, Pokemon pokemon) {
    // Note: you should use the new_pokenode function here, and add
    // the newly-created pokenode to the end of the linked list of
    // pokenodes in the Pokedex.
    struct pokenode *new_pokemon = new_pokenode(pokemon);
    // Found the position the new Pokemon added.
    // Assume there are Pokemons exist
    // and put the new Pokemon after the last existing one.
    if (pokedex->head != NULL) {
        struct pokenode *n = pokedex->head;
        while (n->next != NULL) {
            n = n->next;
        }
        n->next = new_pokemon;
        new_pokemon->previous = n;
    // Assume there are no pokemons exist
    // and let the new Pokemon to be the first one.
    } else {
        pokedex->head = new_pokemon;
        pokedex->cur_pokemon = new_pokemon;
    }
}

// Print out the details of the currently selected Pokemon.
void detail_pokemon(Pokedex pokedex) {
    // Assume pokedex is not empty
    if (pokedex->head != NULL) {
        // Assume the selected Pokemon can be found
        // show details of the this Pokemon
        // which includes ID, Name, Height, Weight and Type
        if (pokedex->cur_pokemon->found == 1) {
            printf("ID: %.3d\n", pokemon_id(pokedex->cur_pokemon->pokemon));
            printf("Name: %s\n", pokemon_name(pokedex->cur_pokemon->pokemon));
            printf("Height: %.1lfm\n", pokemon_height(pokedex->cur_pokemon->pokemon));
            printf("Weight: %.1lfkg\n", pokemon_weight(pokedex->cur_pokemon->pokemon));
            printf("Type: %s ", pokemon_type_to_string(pokemon_first_type(pokedex->cur_pokemon->pokemon)));
            if (pokemon_second_type(pokedex->cur_pokemon->pokemon) != NONE_TYPE) {
                printf("%s\n", pokemon_type_to_string(pokemon_second_type(pokedex->cur_pokemon->pokemon)));
            } else {
                printf("\n");
            }
        // Assume the selected Pokemon cannot be found
        // just show ID of this Pokemon
        } else {
            printf("ID: %.3d\n",  pokemon_id(pokedex->cur_pokemon->pokemon));
            printf("Name: ");
            int counter = 0;
            while (pokemon_name(pokedex->cur_pokemon->pokemon)[counter] != '\0') {
                printf("*");
                counter++;
            }
            printf("\n");
            printf("Height: --\n");
            printf("Weight: --\n");
            printf("Type: --\n");
        }
    }
}

// Return the currently selected Pokemon.
Pokemon get_current_pokemon(Pokedex pokedex) {
    // When the Pokedex is empty
    // print error message and exit the program
    if (pokedex->head == NULL) {
        fprintf(stderr, "Pokedex is empty.\n");
        exit(1);
    // Show the selected Pokemon
    } else {
        return pokedex->cur_pokemon->pokemon;
    }
}

// Sets the currently selected Pokemon to be 'found'.
void find_current_pokemon(Pokedex pokedex) {
    // When the Pokedex is not empty
    // 1 means this Pokemon can be found
    if (pokedex->head != NULL) {
        pokedex->cur_pokemon->found = 1;
    }
}

// Print out all of the Pokemon in the Pokedex.
void print_pokemon(Pokedex pokedex) {
    struct pokenode *n = pokedex->head;
    // Loop all existing Pokemons
    // to print all Pokemon in the Pokedex
     while (n != NULL) {
        if (n == pokedex->cur_pokemon) {
            printf("--> ");
        } else {
            printf("    ");
        }
        // Dispaly Pokemon ID
        // without less than 3 significant figures
        printf("#%.3d: ", pokemon_id(n->pokemon));
        // If the selected Pokemon can be found
        // Output the name
        if (n->found == 1) {
            printf("%s\n", pokemon_name(n->pokemon));
        } else {
            int counter = 0;
            while (pokemon_name(n->pokemon)[counter] != '\0') {
                printf("*");
                counter++;
            }
            printf("\n");
        }
        n = n->next;
    }
}

//////////////////////////////////////////////////////////////////////
//                         Stage 2 Functions                        //
//////////////////////////////////////////////////////////////////////

// Change the currently selected Pokemon to be the next Pokemon in the Pokedex.
void next_pokemon(Pokedex pokedex) {
    if (pokedex->head != NULL) {
        // Assume the next Pokemon exists
        if (pokedex->cur_pokemon->next != NULL) {
            pokedex->cur_pokemon = pokedex->cur_pokemon->next;
        }
    }
}

// Change the currently selected Pokemon to be the previous Pokemon in the Pokedex.
void prev_pokemon(Pokedex pokedex) {
    if (pokedex->head != NULL) {
        // Assume the previous Pokemon exists
        if (pokedex->cur_pokemon->previous != NULL) {
            pokedex->cur_pokemon = pokedex->cur_pokemon->previous;
        }
    }
}

// Change the currently selected Pokemon to be the Pokemon with the ID `id`.
void change_current_pokemon(Pokedex pokedex, int id) {
    struct pokenode *n = pokedex->head;
    // Loop all the Pokemon
    while (n != NULL) {
        // Find which Pokemon is matching given ID
        if (pokemon_id(n->pokemon) == id) {
            pokedex->cur_pokemon = n;
        }
        n = n->next;
    }
}

// Remove the currently selected Pokemon from the Pokedex.
void remove_pokemon(Pokedex pokedex) {
    struct pokenode *n = pokedex->cur_pokemon;
    // Assume is not removing the last Pokemon
    if (n != NULL && n->next != NULL) {
        // Assume is not removing the first Pokemon
        if (pokedex->cur_pokemon->previous != NULL) {
            n->previous->next = n->next;
            pokedex->cur_pokemon = n->next;
            n->next->previous = n->previous;
            destroy_pokemon(n->pokemon);
            free(n);
        // Assume is removing the first Pokemon
        } else {
            pokedex->head = n->next;
            pokedex->cur_pokemon = n->next;
            n->next->previous = n->previous;
            destroy_pokemon(n->pokemon);
            free(n);
        }
    // Aussume is removing the last Pokemon
    } else if (n != NULL && n->next == NULL) {
        if (pokedex->cur_pokemon->previous != NULL) {
            pokedex->cur_pokemon->previous->next = NULL;
            pokedex->cur_pokemon = pokedex->cur_pokemon->previous;
            destroy_pokemon(n->pokemon);
            free(n);
        } else {
            pokedex->head = NULL;
            pokedex->cur_pokemon = NULL;
            destroy_pokemon(n->pokemon);
            free(n);
        }
    }
    
}

// Destroy the given Pokedex and free all associated memory.
void destroy_pokedex(Pokedex pokedex) {
    // Note: there is no fprintf or exit(1) in this function, as the
    // Stage 1 autotests call destroy_pokedex but don't check whether
    // the memory has been freed (so this function should do nothing in
    // Stage 1, rather than exit).
    struct pokenode *n = pokedex->head;
    struct pokenode *previous = NULL;
    // Loop all the Pokemon
    // and free all of them
    while (n != NULL) {
        previous = n;
        n = n->next;
        destroy_pokemon(previous->pokemon);
        free(previous);
    }
    free(pokedex);
}

//////////////////////////////////////////////////////////////////////
//                         Stage 3 Functions                        //
//////////////////////////////////////////////////////////////////////

// Print out all of the different types of Pokemon in the Pokedex.
void show_types(Pokedex pokedex) {
    // Put all types into a new pokedex
    Pokedex typedex = new_pokedex();
    struct pokenode *n = pokedex->head;
    while (n != NULL) {
        if (is_new_type(pokemon_first_type(n->pokemon), typedex) && pokemon_first_type(n->pokemon) != NONE_TYPE) {
            printf("%s\n", pokemon_type_to_string(pokemon_first_type(n->pokemon)));
            if (is_new_type(pokemon_second_type(n->pokemon), typedex) && pokemon_second_type(n->pokemon) != NONE_TYPE) {
                printf("%s\n", pokemon_type_to_string(pokemon_second_type(n->pokemon)));
            }
            add_pokemon(typedex, clone_pokemon(n->pokemon));
        }
        if (is_new_type(pokemon_second_type(n->pokemon), typedex) && pokemon_second_type(n->pokemon) != NONE_TYPE) {
            printf("%s\n", pokemon_type_to_string(pokemon_second_type(n->pokemon)));
            add_pokemon(typedex, clone_pokemon(n->pokemon));
        }
        n = n->next;
    }
    destroy_pokedex(typedex);
}

// Set the first not-yet-found Pokemon of each type to be found.
void go_exploring(Pokedex pokedex) {
    // Put all no found Pokemon into a new pokedex
    Pokedex no_found_pokemon = new_pokedex();
    struct pokenode *n = pokedex->head;
    while (n != NULL) {
        if (n->found == 0) {
            add_pokemon(no_found_pokemon, clone_pokemon(n->pokemon));
        }
        n = n->next;
    }
    Pokedex typedex = new_pokedex();
    n = no_found_pokemon->head;
    while (n != NULL) {
        if (is_new_type(pokemon_first_type(n->pokemon), typedex) && pokemon_first_type(n->pokemon) != NONE_TYPE) {
            add_pokemon(typedex, clone_pokemon(n->pokemon));
        }
        if (is_new_type(pokemon_second_type(n->pokemon), typedex) && pokemon_second_type(n->pokemon) != NONE_TYPE) {
            add_pokemon(typedex, clone_pokemon(n->pokemon));
        }
        n = n->next;
    }
    n = typedex->head;
    struct pokenode *cur = pokedex->cur_pokemon;
    while (n != NULL) {
        change_current_pokemon(pokedex, pokemon_id(n->pokemon));
        find_current_pokemon(pokedex);
        n = n->next;
    }
    pokedex->cur_pokemon = cur;
    destroy_pokedex(no_found_pokemon);
    destroy_pokedex(typedex);
}

// Return the total number of Pokemon in the Pokedex.
int count_total_pokemon(Pokedex pokedex) {
    struct pokenode *n = pokedex->head;
    int index = 0;
    // Loop all Pokemons
    // to count them
    while (n != NULL) {
        index++;
        n = n->next;
    }
    return index;
}

// Return the number of Pokemon in the Pokedex that have been found.
int count_found_pokemon(Pokedex pokedex) {
    struct pokenode *n = pokedex->head;
    int index = 0;
    // Loop all Pokemons
    while (n != NULL) {
        // Assume the Pokemon can be found
        // count them
        if(n->found == 1) {
            index++;
        }
        n = n->next;
    }
    return index;
}

//////////////////////////////////////////////////////////////////////
//                         Stage 4 Functions                        //
//////////////////////////////////////////////////////////////////////

// Add the information that the Pokemon with the ID `from_id` can
// evolve into the Pokemon with the ID `to_id`.
void add_pokemon_evolution(Pokedex pokedex, int from_id, int to_id) {
    struct pokenode *n = pokedex->head;
    // Exclude the evolution ID is same as orginal ID
    // put out error message
    // exit the program
    if (from_id == to_id) {
        fprintf(stderr, "exiting because from_id is same as to_id.\n");
        exit(1);
    }
    // Loop all the Pokemon
    while (n != NULL) {
        // Find which Pokemon is matching given ID
        if (pokemon_id(n->pokemon) == from_id) {
            n->evolve_id = to_id;
        }
        n = n->next;
    }
}

// Show the evolutions of the currently selected Pokemon.
void show_evolutions(Pokedex pokedex) {
    if (pokedex->head != NULL) {
        printf("#%.3d ", pokemon_id(pokedex->cur_pokemon->pokemon));
        // Assume the orginal Pokemon can be found
        if (pokedex->cur_pokemon->found == 1) {
            printf("%s [%s", pokemon_name(pokedex->cur_pokemon->pokemon), pokemon_type_to_string(pokemon_first_type(pokedex->cur_pokemon->pokemon)));
            if (pokemon_second_type(pokedex->cur_pokemon->pokemon) != NONE_TYPE) {
                printf(" %s]", pokemon_type_to_string(pokemon_second_type(pokedex->cur_pokemon->pokemon)));
            } else{
                printf("]");
            }
        // Assume the orginal Pokemon cannot be found
        } else {
            printf("???? [????]");
        }
        int target_id = pokedex->cur_pokemon->evolve_id;
        // print evolution
        // by looping and finding evolve_id
        while (target_id != DOES_NOT_EVOLVE) {
            struct pokenode *n = pokedex->head;
            while (n != NULL) {
                if (pokemon_id(n->pokemon) == target_id) {
                    printf(" --> ");
                    printf("#%.3d ", pokemon_id(n->pokemon));
                    if (n->found == 1) {
                        printf("%s [%s", pokemon_name(n->pokemon), pokemon_type_to_string(pokemon_first_type(n->pokemon)));
                        if (pokemon_second_type(n->pokemon) != NONE_TYPE) {
                            printf(" %s]", pokemon_type_to_string(pokemon_second_type(n->pokemon)));
                        } else{
                            printf("]");
                        }
                    } else {
                        printf("???? [????]");
                    }
                    target_id = n->evolve_id;
                }
                n = n->next;
            }
        }
        printf("\n");
    }
}

// Return the pokemon_id of the Pokemon that the currently selected
// Pokemon evolves into.
int get_next_evolution(Pokedex pokedex) {
    if (pokedex->head != NULL) {
        return pokedex->cur_pokemon->evolve_id;
    } else {
        fprintf(stderr, "pokedex is empty\n");
        exit(1);
    }
}

//////////////////////////////////////////////////////////////////////
//                         Stage 5 Functions                        //
//////////////////////////////////////////////////////////////////////

// Create a new Pokedex which contains only the Pokemon of a specified
// type from the original Pokedex.
Pokedex get_pokemon_of_type(Pokedex pokedex, pokemon_type type) {
    fprintf(stderr, "exiting because you have not implemented the get_pokemon_of_type function\n");
    exit(1);
}

// Create a new Pokedex which contains only the Pokemon that have
// previously been 'found' from the original Pokedex.
Pokedex get_found_pokemon(Pokedex pokedex) {
    fprintf(stderr, "exiting because you have not implemented the get_found_pokemon function\n");
    exit(1);
}

// Create a new Pokedex containing only the Pokemon from the original
// Pokedex which have the given string appearing in its name.
Pokedex search_pokemon(Pokedex pokedex, char *text) {
    fprintf(stderr, "exiting because you have not implemented the search_pokemon function\n");
    exit(1);
}

// Add definitions for your own functions here.
// Make them static to limit their scope to this file.

// Determine whether type is not existing in typedex
// If true, return 1, if false, return 0
int is_new_type(pokemon_type type, Pokedex typedex) {
    if (typedex->head != NULL) {
        struct pokenode *n = typedex->head;
        while (n != NULL) {
            if (type == pokemon_first_type(n->pokemon)) {
                return 0;
            }
            if (type == pokemon_second_type(n->pokemon)) {
                return 0;
            }
            n = n->next;
        }
    }
    return 1;
}
