"""
Dichotomous Key for Dog Breed Identification

A dichotomous key uses a series of yes/no branching questions to narrow down
the identification to a specific breed. Each question splits the possibilities
into two groups until a final identification is reached.
"""

# Import UI utilities
try:
    from ui_utils import (
        Colors, print_colored, print_header, print_subheader,
        print_success, print_error, print_warning, print_info,
        print_divider, print_box, get_input, print_result_card
    )
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    class Colors:
        RESET = BOLD = BRIGHT_WHITE = BRIGHT_CYAN = BRIGHT_YELLOW = BRIGHT_GREEN = BRIGHT_RED = DIM = BRIGHT_MAGENTA = ""


class DichotomousKey:
    def __init__(self):
        # Build the decision tree for dog breed identification
        self.tree = self._build_tree()
        self.question_count = 0

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
        if UI_AVAILABLE:
            print()
            print(f"  {Colors.BRIGHT_MAGENTA}Q{self.question_count}:{Colors.RESET} {Colors.BRIGHT_WHITE}{question}{Colors.RESET}")
            print()
            print(f"      {Colors.BRIGHT_GREEN}[Y]{Colors.RESET} {Colors.BRIGHT_WHITE}Yes{Colors.RESET}     {Colors.BRIGHT_RED}[N]{Colors.RESET} {Colors.BRIGHT_WHITE}No{Colors.RESET}")
            print()
        else:
            print(f"\n{question}")
            print("  [Y] Yes")
            print("  [N] No")

        while True:
            if UI_AVAILABLE:
                response = input(f"  {Colors.BRIGHT_CYAN}▶{Colors.RESET} {Colors.BRIGHT_WHITE}Your answer:{Colors.RESET} ").strip().lower()
            else:
                response = input("\nYour answer (Y/N): ").strip().lower()

            if response in ['y', 'yes']:
                if UI_AVAILABLE:
                    print(f"      {Colors.BRIGHT_GREEN}✓ Yes{Colors.RESET}")
                return True
            elif response in ['n', 'no']:
                if UI_AVAILABLE:
                    print(f"      {Colors.BRIGHT_RED}✓ No{Colors.RESET}")
                return False
            else:
                if UI_AVAILABLE:
                    print(f"      {Colors.BRIGHT_YELLOW}⚠ Please enter Y for Yes or N for No{Colors.RESET}")
                else:
                    print("Please enter Y for Yes or N for No.")

    def identify(self):
        """Run the dichotomous key identification process.

        Returns:
            str: The identified breed name, or None if multiple matches
        """
        if not UI_AVAILABLE:
            print("\n" + "=" * 55)
            print("       DICHOTOMOUS KEY - Dog Breed Identifier")
            print("=" * 55)
            print("\nAnswer the following Yes/No questions to identify your dog.")
            print("This method uses a branching decision tree to narrow down")
            print("the breed based on physical characteristics.\n")

        current_node = self.tree
        self.question_count = 0
        result_breed = None

        while True:
            if "result" in current_node:
                # We've reached a final identification
                result_breed = current_node['result']
                if UI_AVAILABLE:
                    print()
                    print_divider("═", 60, Colors.BRIGHT_GREEN)
                    print()
                    print(f"  {Colors.BRIGHT_GREEN}🎉 IDENTIFICATION COMPLETE!{Colors.RESET}")
                    print()
                    print(f"  {Colors.DIM}Based on {self.question_count} questions:{Colors.RESET}")
                    print()
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}╔{'═' * 50}╗{Colors.RESET}")
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_WHITE}🐕 Your dog is most likely a:{Colors.RESET}")
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.RESET}     {Colors.BOLD}{Colors.BRIGHT_YELLOW}{result_breed}{Colors.RESET}")
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
                    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}╚{'═' * 50}╝{Colors.RESET}")
                    print()
                    print_divider("═", 60, Colors.BRIGHT_GREEN)
                else:
                    print("\n" + "=" * 55)
                    print("              IDENTIFICATION RESULT")
                    print("=" * 55)
                    print(f"\nBased on your answers ({self.question_count} questions):")
                    print(f"\n  >>> {result_breed} <<<")
                    print("\n" + "=" * 55)
                break

            elif "results" in current_node:
                # Multiple possible results - return the first one
                result_breed = current_node['results'][0] if current_node['results'] else None
                if UI_AVAILABLE:
                    print()
                    print_divider("═", 60, Colors.BRIGHT_YELLOW)
                    print()
                    print(f"  {Colors.BRIGHT_YELLOW}🔍 MULTIPLE MATCHES FOUND{Colors.RESET}")
                    print()
                    print(f"  {Colors.DIM}Based on {self.question_count} questions, your dog could be:{Colors.RESET}")
                    print()
                    for breed in current_node['results']:
                        print(f"      {Colors.BRIGHT_CYAN}•{Colors.RESET} {Colors.BRIGHT_WHITE}{breed}{Colors.RESET}")
                    print()
                    print_divider("═", 60, Colors.BRIGHT_YELLOW)
                else:
                    print("\n" + "=" * 55)
                    print("            POSSIBLE IDENTIFICATIONS")
                    print("=" * 55)
                    print(f"\nBased on your answers ({self.question_count} questions):")
                    print("\nYour dog could be one of:")
                    for breed in current_node['results']:
                        print(f"  • {breed}")
                    print("\n" + "=" * 55)
                break

            elif "question" in current_node:
                self.question_count += 1
                answer = self.ask_yes_no(current_node['question'])
                current_node = current_node["yes"] if answer else current_node["no"]
            else:
                if UI_AVAILABLE:
                    print_error("Error in decision tree structure.")
                else:
                    print("Error in decision tree structure.")
                break

        return result_breed


def run_dichotomous_key():
    """Convenience function to run the dichotomous key identifier."""
    key = DichotomousKey()
    key.identify()


if __name__ == "__main__":
    run_dichotomous_key()
