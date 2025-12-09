"""
Dichotomous Key for Dog Breed Identification

A dichotomous key uses a series of yes/no branching questions to narrow down
the identification to a specific breed. Each question splits the possibilities
into two groups until a final identification is reached.
"""


class DichotomousKey:
    def __init__(self):
        # Build the decision tree for dog breed identification
        self.tree = self._build_tree()

    def _build_tree(self):
        """
        Build a dichotomous key decision tree.
        Each node is either:
        - A question node: {"question": str, "yes": node, "no": node}
        - A result node: {"result": str} or {"results": [str, ...]}
        """
        return {
            "question": "Is your dog SMALL (under 25 lbs)?",
            "yes": {
                "question": "Does your dog have FLOPPY ears (hanging down)?",
                "yes": {
                    "question": "Does your dog have a LONG coat?",
                    "yes": {
                        "question": "Does your dog have a CURLED tail?",
                        "yes": {"result": "Shih Tzu"},
                        "no": {"result": "Shetland Sheepdog"}
                    },
                    "no": {
                        "question": "Does your dog have a SILKY coat?",
                        "yes": {"result": "Cavalier King Charles Spaniel"},
                        "no": {
                            "question": "Does your dog have a CURLED tail?",
                            "yes": {"result": "Dachshund (smooth coat)"},
                            "no": {"result": "Dachshund"}
                        }
                    }
                },
                "no": {
                    "question": "Does your dog have TRIANGULAR (pointed/erect) ears?",
                    "yes": {
                        "question": "Does your dog have a LONG coat?",
                        "yes": {"result": "Pomeranian"},
                        "no": {
                            "question": "Does your dog have a SILKY coat?",
                            "yes": {
                                "question": "Does your dog have a DOCKED tail?",
                                "yes": {"result": "Yorkshire Terrier"},
                                "no": {"result": "Maltese"}
                            },
                            "no": {
                                "question": "Does your dog have a SMOOTH coat?",
                                "yes": {"result": "Pug"},
                                "no": {
                                    "question": "Does your dog have a SHORT coat?",
                                    "yes": {"result": "Boston Terrier or Chihuahua"},
                                    "no": {"result": "Chihuahua (long coat)"}
                                }
                            }
                        }
                    },
                    "no": {
                        "question": "Does your dog have TALL (upright) ears?",
                        "yes": {"result": "Small mixed breed (tall ears uncommon in small purebreds)"},
                        "no": {"result": "Small mixed breed"}
                    }
                }
            },
            "no": {
                "question": "Is your dog GIANT sized (over 100 lbs)?",
                "yes": {
                    "question": "Does your dog have a SHORT coat?",
                    "yes": {"result": "Great Dane"},
                    "no": {"result": "Saint Bernard"}
                },
                "no": {
                    "question": "Is your dog LARGE (50-100 lbs)?",
                    "yes": {
                        "question": "Does your dog have FLOPPY ears?",
                        "yes": {
                            "question": "Does your dog have a LONG coat?",
                            "yes": {"result": "Bernese Mountain Dog"},
                            "no": {
                                "question": "Does your dog have a DENSE coat?",
                                "yes": {"result": "Rottweiler"},
                                "no": {
                                    "question": "Does your dog have a DOUBLE coat?",
                                    "yes": {"result": "Siberian Husky"},
                                    "no": {
                                        "question": "Does your dog have a DOCKED tail?",
                                        "yes": {"result": "Rottweiler or Doberman Pinscher"},
                                        "no": {
                                            "question": "Does your dog have a MEDIUM length coat?",
                                            "yes": {"result": "English Setter"},
                                            "no": {"result": "Boxer or Labrador Retriever"}
                                        }
                                    }
                                }
                            }
                        },
                        "no": {
                            "question": "Does your dog have TALL (upright) ears?",
                            "yes": {
                                "question": "Does your dog have a DOCKED tail?",
                                "yes": {"result": "Doberman Pinscher"},
                                "no": {
                                    "question": "Does your dog have a SHORT coat?",
                                    "yes": {"result": "Boxer or Great Dane"},
                                    "no": {"result": "German Shepherd (not in database)"}
                                }
                            },
                            "no": {
                                "question": "Does your dog have TRIANGULAR ears?",
                                "yes": {"result": "Siberian Husky"},
                                "no": {"result": "Large mixed breed"}
                            }
                        }
                    },
                    "no": {
                        # Medium sized dogs
                        "question": "Does your dog have FLOPPY ears?",
                        "yes": {
                            "question": "Does your dog have a CURLY coat?",
                            "yes": {"result": "Poodle"},
                            "no": {
                                "question": "Does your dog have a SILKY coat?",
                                "yes": {"result": "Cocker Spaniel"},
                                "no": {
                                    "question": "Does your dog have a MEDIUM length coat?",
                                    "yes": {
                                        "question": "Does your dog have a CURLED tail?",
                                        "yes": {"result": "Australian Shepherd"},
                                        "no": {"result": "Border Collie"}
                                    },
                                    "no": {
                                        "question": "Does your dog have a SHORT coat?",
                                        "yes": {"result": "Basset Hound or Beagle"},
                                        "no": {"result": "Medium mixed breed"}
                                    }
                                }
                            }
                        },
                        "no": {
                            "question": "Does your dog have TRIANGULAR ears?",
                            "yes": {
                                "question": "Does your dog have a DOUBLE coat?",
                                "yes": {"result": "Shiba Inu"},
                                "no": {
                                    "question": "Does your dog have a DENSE coat?",
                                    "yes": {"result": "Chow Chow"},
                                    "no": {"result": "Shiba Inu or Basenji"}
                                }
                            },
                            "no": {
                                "question": "Does your dog have TALL ears?",
                                "yes": {"result": "Medium mixed breed (tall ears)"},
                                "no": {"result": "Medium mixed breed"}
                            }
                        }
                    }
                }
            }
        }

    def ask_yes_no(self, question):
        """Ask a yes/no question and return the boolean result."""
        print(f"\n{question}")
        print("  [Y] Yes")
        print("  [N] No")

        while True:
            response = input("\nYour answer (Y/N): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter Y for Yes or N for No.")

    def identify(self):
        """Run the dichotomous key identification process."""
        print("\n" + "=" * 55)
        print("       DICHOTOMOUS KEY - Dog Breed Identifier")
        print("=" * 55)
        print("\nAnswer the following Yes/No questions to identify your dog.")
        print("This method uses a branching decision tree to narrow down")
        print("the breed based on physical characteristics.\n")

        current_node = self.tree
        question_count = 0

        while True:
            if "result" in current_node:
                # We've reached a final identification
                print("\n" + "=" * 55)
                print("              IDENTIFICATION RESULT")
                print("=" * 55)
                print(f"\nBased on your answers ({question_count} questions):")
                print(f"\n  >>> {current_node['result']} <<<")
                print("\n" + "=" * 55)
                break
            elif "results" in current_node:
                # Multiple possible results
                print("\n" + "=" * 55)
                print("            POSSIBLE IDENTIFICATIONS")
                print("=" * 55)
                print(f"\nBased on your answers ({question_count} questions):")
                print("\nYour dog could be one of:")
                for breed in current_node['results']:
                    print(f"  • {breed}")
                print("\n" + "=" * 55)
                break
            elif "question" in current_node:
                question_count += 1
                answer = self.ask_yes_no(f"Q{question_count}: {current_node['question']}")
                current_node = current_node["yes"] if answer else current_node["no"]
            else:
                print("Error in decision tree structure.")
                break


def run_dichotomous_key():
    """Convenience function to run the dichotomous key identifier."""
    key = DichotomousKey()
    key.identify()


if __name__ == "__main__":
    run_dichotomous_key()
