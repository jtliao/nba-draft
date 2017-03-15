from collections import defaultdict
from operator import itemgetter
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


def build_doc_norms(inv_index_filename, idf_filename, doc_norms_filename):
    with open(inv_index_filename, "r") as f1:
        with open(idf_filename, "r") as f2:
            with open(doc_norms_filename, "w") as f3:
                inv_index = json.load(f1)
                idf = json.load(f2)

                doc_norms = defaultdict(int)

                for term, postings in inv_index.items():
                    for doc_ind, tf in postings:
                        weight_update = (tf * idf[term]) * (tf * idf[term])
                        doc_norms[doc_ind] += weight_update

                json.dump(doc_norms, f3)


def calc_cosine_sim_rankings(sorted_curr_players_filename, inv_index_filename, idf_filename,
                             doc_norms_filename, prospect_to_docs_filename, rankings_file):
    with open(sorted_curr_players_filename, "r") as f1, open(inv_index_filename, "r") as f2, open(idf_filename, "r") as f3:
        with open(prospect_to_docs_filename, "r") as f4, open(doc_norms_filename, "r") as f5, open(rankings_file, "w") as f6:
            doc_norms = json.load(f5)
            sorted_curr_players = json.load(f1)
            inv_index = json.load(f2)
            idf = json.load(f3)

            doc_scores = defaultdict(int)
            prospect_to_rankings = {}

            prospect_to_docs = json.load(f4)
            for prospect, doc in prospect_to_docs.items():
                tokens = nltk.word_tokenize(doc)
                for token in set(tokens):
                    if token in inv_index.keys() and token in idf.keys():
                        postings_list = inv_index[token]
                        for (player_ind, tf) in postings_list:
                            weight_update = (tokens.count(token) * idf[token]) * (tf * idf[token])
                            doc_scores[player_ind] += weight_update

                # PURELY DOING RANKING RIGHT NOW SO DISREGARD QUERY NORM
                for d in doc_scores:
                    doc_scores[d] /= float(doc_norms[str(d)])

                doc_idx_scores = sorted(doc_scores.items(), key=itemgetter(1), reverse=True)[:10]
                rankings = [sorted_curr_players[doc_idx] for doc_idx, score in doc_idx_scores if score > 0]
                print(prospect)
                print(rankings)
                print("\n")
                prospect_to_rankings[prospect] = rankings

            json.dump(prospect_to_rankings, f6)



def main():
    # only run once
    # build_sorted_current_player_name_set("curr_player_to_docs.json", "sorted_curr_players.json")
    # build_curr_players_inv_index("curr_player_to_docs.json", "sorted_curr_players.json", "curr_player_inv_index.json")
    # build_idf("curr_player_inv_index.json", "curr_player_idf.json")
    # build_doc_norms("curr_player_inv_index.json", "curr_player_idf.json", "curr_player_doc_norms.json")

    calc_cosine_sim_rankings("sorted_curr_players.json", "curr_player_inv_index.json", "curr_player_idf.json",
                             "curr_player_doc_norms.json", "prospect_to_docs.json", "prospect_rankings.json")


if __name__ == "__main__":
    main()