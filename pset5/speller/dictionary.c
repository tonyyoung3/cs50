// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include "ctype.h"
#include "string.h"
#include "stdlib.h"
#include "stdio.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Number of buckets in hash table
const unsigned int N = 50;
unsigned int dic_word = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    char lower[strlen(word)];
    for (int i = 0 ; i < strlen(word) ; i++ ) //lower case
    {

        lower[i] = tolower(word[i]);
    }
    lower[strlen(word)] = '\0';

    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next) // go to hash table and check one by one
    {

        // compare
        if (strcmp(lower, tmp -> word) == 0)
        {
            return true;
        }

    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

    int hashvalue = strlen(word);
    return (hashvalue % N) -1;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // List of size 0
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    else
    {


    char* buffer = malloc((LENGTH + 1) * sizeof(char));

    while (fscanf(file , "%s" , buffer) != EOF)
    {
        node *n = malloc(sizeof(node));
        dic_word += 1;
        int x = hash(buffer) ;
        strcpy(n -> word , buffer);
        n -> next = NULL;

        if (table[x] == NULL) //NEW linked list
        {
            table[x] = n ;
        }

        else //insert
        {
            n -> next = table[x] ;

            table[x] = n ;

        }


    }

    //free(n);
    free(buffer);
    fclose(file);

    return true;
    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dic_word;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    // TODO
    int check = 0;
    for (int i = 0 ; i < N ; i++)
    {
        
        //printf("%i\n" , i);
        
        while(table[i] != NULL)
        {
            node *tmp = table[i];
            //printf("%s\n" , table[i] -> word );
            node *cursor = tmp ->next;
            free(tmp) ;
            table[i] = cursor ;
            //printf("--post--\n");
            //printf("%s" , table[i] -> word);
        }
        
        
        check ++ ;
        if(check == N)
        {
            return true;
        }
    }


    return false;
}
