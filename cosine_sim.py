from collections import defaultdict
import json
import nltk


def build_sorted_current_player_name_set(player_to_docs_filename, output_filename):
    with open(player_to_docs_filename, "r") as f:
        player_to_docs = json.load(f)
        valid_player_names = []
        for player_name, doc in sorted(player_to_docs.items()):
            if len(player_name) > 0 and len(doc) > 0:
                valid_player_names.append(player_name)

        with open(output_filename, "w") as f2:
            json.dump(valid_player_names, f2)


def build_curr_players_inv_index(player_to_docs_filename, sorted_player_names_filename, inv_index_filename):
    with open(player_to_docs_filename, "r") as f1:
        with open(sorted_player_names_filename, "r") as f2:
            player_to_docs = json.load(f1)
            sorted_player_names = json.load(f2)

            term_to_player_ind = defaultdict(list)

            for player_name, doc in player_to_docs.items():
                print(player_name)

                if player_name in sorted_player_names:
                    tokens = nltk.word_tokenize(doc)
                    for token in set(tokens):
                        term_to_player_ind[token].append((sorted_player_names.index(player_name), tokens.count(token)))

            with open(inv_index_filename, "w") as f3:
                json.dump(term_to_player_ind, f3)


def build_idf(inv_index_filename, idf_filename):
    with open(inv_index_filename, "r") as f1:
        idf = {}

        inv_index = json.load(f1)
        for term, postings_list in inv_index.items():
            idf[term] = 1 / float(len(postings_list) + 1)

        with open(idf_filename, "w") as f2:
            json.dump(idf, f2)


def calc_cosine_sim_rankings(inv_index_filename, idf_filename, prospect_to_docs_filename):
    with open(inv_index_filename, "r") as f1:
        with open(idf_filename, "r") as f2:
            with open(prospect_to_docs_filename, "r") as f3:
                prospect_to_docs = json.load(f3)
                for prospect, doc_list in prospect_to_docs.items():
                    for doc in doc_list:
                        tokens = nltk.word_tokenize(doc)



def main():
    # only run once
    build_sorted_current_player_name_set("curr_player_to_docs.json", "sorted_curr_players.json")
    build_curr_players_inv_index("curr_player_to_docs.json", "sorted_curr_players.json", "curr_player_inv_index.json")
    build_idf("curr_player_inv_index.json", "curr_player_idf.json")


if __name__ == "__main__":
    main()