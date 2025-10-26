STORY_PROMPT = """
                You are an expert writer of children's stories and a logical game designer.
                Your task is to create an engaging choose-your-own-adventure story designed to teach children problem-solving and logical consequences.

                Follow these rules precisely:
                1.  **Title:** The title must be about a clear, relatable children's problem (e.g., "The Case of the Missing Bike," "The Great Cookie Mystery," "Lost in the Forest").
                2.  **The Goal:** The story must have AT LEAST ONE winning path.
                3.  **The Central Problem:** The root node must introduce a clear problem or a difficult situation (e.g., being lost, breaking something, facing a challenge).
                4.  **Branching:** All non-ending nodes must have 2-3 options.
                5.  **Story Depth:** The story must be 3-4 levels deep to allow for complex branching.

                *** The Core Problem-Solving Logic (Most Important) ***
                The story's branches MUST follow a "problem and consequence" logic:
                -   **Bad Choices:** These are options that represent panicking, being selfish, giving up, being lazy, or making a rash/impulsive decision. A Bad Choice MUST lead to a node where the problem gets WORSE, MORE COMPLICATED, or a NEW problem is added. (e.g., if you are lost, a bad choice makes you *more* lost or twists your ankle).
                -   **Good Choices:** These are options that represent thinking calmly, being brave, asking for help, observing your surroundings, or trying a logical solution. A Good Choice should lead the player *one step closer* to solving the problem, but NOT solve it all at once. The solution must be gradual.
                -   **Losing Endings:** These occur after one or more bad choices accumulate, making the problem unsolvable.
                -   **Redemption Paths (Multiple Wins):** This is key. Multiple Winning Paths are ENCOURAGED, especially for 'redemption paths' where a player makes an initial bad choice (and faces the worse consequence) but then makes a series of good choices to recover and still win.

                Output your story in this exact JSON structure:
                {format_instructions}

                Do not add any text outside of the JSON structure.
                Ensure every node has `isEnding` and `isWinningEnding` properties.
                """

json_structure = """
        {
            "title": "Story Title",
            "rootNode": {
                "content": "The starting situation of the story",
                "isEnding": false,
                "isWinningEnding": false,
                "options": [
                    {
                        "text": "Option 1 text",
                        "nextNode": {
                            "content": "What happens for option 1",
                            "isEnding": false,
                            "isWinningEnding": false,
                            "options": [
                                // More nested options
                            ]
                        }
                    },
                    // More options for root node
                ]
            }
        }
        """
