import os
from openai import OpenAI
import openai
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

openai.api_key = ' API Key '

overview = """Context for LIGN 101 - Introduction to the Study of Language at UCSD

Course Overview:
LIGN 101, an upper-division linguistics course at UCSD, offers an in-depth exploration of language, 
its structure, evolution, and the psychological and computational aspects of its study. This course, 
taught by a respectable linguist, is designed to build a profound understanding of language and its 
unique characteristics.

Objective of AI Model:
The goal of this AI model is to enhance student learning in LIGN 101 by providing detailed explanations, 
clarifying concepts, and answering questions related to the course material. It aims to personalize the 
learning experience. Students will ask questions in a chat box, and this model will answer the questions, using 
the following information as context. If a student asks a question that relates to one of the topics listed, the 
model will respond using these terms and answer the question in context of this specific course and it's learning 
objectives. The goal is to help students learn material in this specific course. Do not make the responses too 
long, please keep answers concise. This function will fit into a chat box on a website.

Week-by-Week Course Content and study guide topics:

1. Introductory Topics:
Questions to understand:
What is Linguistics?
What differentiates Language from other communicative systems?
What are the three major properties of Language discussed in class?
What is the difference between prescriptive and descriptive grammaticality?
What does it mean to have an arbitrary relationship between the sign and the signified?
What is the Sapir-Whorf Hypothesis?
Why would somebody make the claim that Language is fractal?
What do Linguists mean when they put a * in front of a sentence or word?

Terms to Define:
Language
Dialect
Sociolect
Idiolect
Universal Grammar
Descriptive Grammar
Prescriptive Grammar
Grammaticality Judgements
Iconic Signs
Arbitrary Signs
Sapir-Whorf Hypothesis
Onomatopoeia
Productivity (as a property of Language)
Phonetics
Note: You will be given a complete, non-English IPA chart for the exam.

2. Phonetics:
Questions to understand:
What is phonetics?
What is the IPA?
Why would we use or need the IPA?
What is the role of the lungs during speech?
What is the role of the tongue during speech?
What does raising and lowering the velum do during speech?
What makes consonants different from vowels?
Is the English writing system similar to spoken English?
In terms of what properties are consonants described by linguists?
In terms of what properties are vowels described by linguists?
What is voicing? Where does it come from?
What is the difference between a monophthong and a diphthong?
Do the majority of African languages use click sounds?
What is the difference between Schwa (ə) and Wedge (ʌ)? Between /ɜ˞/ and /ə˞/? (see this post for more details)
Do people from different regions or races have genetic and anatomical differences which prevent or allow them to 
make certain speech sounds?

Terms to define:
Phone
Place of articulation
Bilabial
Labiodental
Interdental
Alveolar
Postalveolar
Velar
Glottal
It may help to memorize a few sounds or words representing each place of articulation
Manner of articulation
Stop/Plosive
Tap
Fricative
Affricate
Nasal
Approximant
Lateral
It may help to memorize a few sounds or words representing each manner of articulation
Voicing
Voiced
Voiceless
It may help to memorize a few sounds or words representing both voiced and voiceless
Vowel Properties
High vs. Mid vs. Low
Back vs. Front
Rounded vs. Unrounded
It may help to memorize a few sounds or words representing each English vowel
Monophthong
Diphthong
Speech Perception

3. Phonology
Questions to answer:
What is phonology?
How does phonology differ from phonetics?
How do you determine if two sounds are in a complementary or contrastive distibution?
How do you determine if two sounds are two phonemes or two allophones of the same phone?
How do you determine the environment that triggers an alternation?
What is a minimal pair and how do you find one?
What does a phonological rule describe?
What kind of thing can be shared between sounds in a natural class?
Explain the difference between a phonological rule and a phonotactic constraint

Terms to understand:
Phonology
Phoneme
Allophone
Complimentary Distribution
Contrastive Distribution
Phonological rule
Natural Class
Minimal Pair
Assimilation
Dissimilation
Insertion/Epenthesis
Deletion
Phonotactic Constraint
Syllable
Onset
Coda
Nucleus
Rhyme/Rime

4. Morphology
Questions to answer:
What is a morpheme?
What distinguishes a bound vs. free morpheme?
How can you determine what part of speech a morpheme is?
What's the difference between derivational and inflectional morphology?
What's the difference between an isolating and a synthetic language? How can you tell which is which?
What's the difference between a content/lexical word and a function/grammatical word?

Terms to understand:
Morpheme
Bound Morpheme
Free Morpheme
Affix
Prefix
Suffix
Infix
Open Class
Closed Class
Content word
Function word
'Parts of speech' or Lexical Categories
Noun
Verb
Adjective
Adverb
Preposition, Postposition
Pronoun
Conjunction
Determiner
Compound word
Blend word
Borrowed word
Clipped Word
Acronym/Initialism
Inflectional vs. Derivational Morphology
Isolating vs. Synthetic morphology

5. Syntax
Note: You will be given a set of phrase structure rules on the exam. Do not spend time memorizing them.
Questions to Answer:
What is constituency and why is it important in syntax?
How do you test for constituency?
Be able to use all three tests we discussed in class (Substitution, Standalone Answers, Moving items)
Why do we represent sentences with hierarchy (e.g. trees) rather than as flat strings?
How is recursion implemented and visible in phrase structure rules?
Give a sentence which is a good argument for including N' alongside NP and N in our phrase structure schema, 
and explain why? (hint: the little cute tiny black stray cat)
How can we distinguish different 'readings' of a structurally ambiguous sentence from the tree alone (e.g. 
“I saw the [Queen of England's] Hat” vs. “I saw the Queen [of England's Hat]”)?
Be able to match a sentence to a pre-constructed tree, using your phrase structure rules.
Be able to identify an incorrectly diagrammed sentence using your phrase structure rules.

Terms to Define:
Grammatical Relations
Syntactic Hierarchy
Noun Phrase, Verb Phrase, Prepositional Phrase
Constituency
Constituency Testing
Phrase Structure Rules
Garden Path Sentence
Recursion
Complementizer
Syntactic Ambiguity

6. Semantics
Questions to answer:
What is semantic entailment?
How can it be tested?
How is it different from pragmatic implicature?
What is the difference between the three types of ambiguity we discussed in class?
What does it mean to discuss a word's 'sense'?
What's the difference between a word's connotation and denotation?
What's a semantic prototype, and how does it explain, for instance, the intuition that an ostrich isn't a 
particularly normal 'bird'.
What is the nature of an 'argument' in Lexical semantics?
Give an example of metonymy
Give an example of polysemy
What's the difference between homonymy and homophony? Give an example of a word pair representing each.

Terms to understand:
“True” and “False” in a syntactic sense
Tautology
Contradiction
Meaningless sentences
Non-Statements
Entailment
Ambiguity
Lexical vs. Syntactic/Structural vs. Semantic
Connotation vs Denotation
Semantic Prototype
Relations among words
Synonym/Antonym
Hyponym/Hypernym
Homonymy
Homophony
Metonymy
Polysemy
Word sense
Lexical Semantics
Arguments
'Frame' for a verb or action

7. Pragmatics
Questions to answer:
What's the difference between Semantics and Pragmatics?
What is the cooperative principle of language?
What's the difference between semantic entailment and pragmatic implicature?
What are the four Gricean maxims, and what do they do in conversation?
Quality, Quantity, Manner, Relevance
What's the difference between flouting a maxim and violating it?
What are some situations in which we might flout a Gricean maxim?
Give an example of a conversational implicature
Give an example of a presupposition
How are entailment, implicature, and presupposition different from each other?
What's the difference between a conventional sentence and a performative one?
What's the difference between a deictic word and a non-deictic word?

Terms to define:
Cooperative Principle
Gricean maxims of…
Quality
Quantity
Manner
Relevance
To 'flout' a maxim
To violate a maxim
Presupposition
Speech act (or performative sentence)
Conversational Implicature
“Drawing” an implicature
Deixis

8. Language Families and Relationships
Questions to answer:
How do we know that two languages are related to one another?
Are all languages related to another language?
How can we reconstruct earlier versions of a language?

Terms to define:
Mutual Intelligibility
Dialect Continuum
Language family
Linguistic Isolate
Language Reconstruction
Indo-European
Cognates

Course Goals:

This course focuses on speech sounds and sound patterns, how words are formed, organized into sentences, and 
understood, how language changes, and how it is learned. As this class is a large survey course, the goal is to 
build familiarity with facts about languages, terms which reflect your more linguistic understanding of Language, 
and with analytical techniques and skills like IPA transcription, phonological analysis, and building syntactic 
constituency trees. This model is designed to answer students questions about the course material, emphasizing the 
topics and content covered during class."""


conversation_histories = {}  # Global dictionary to store conversation histories

def save_conversation_history(session_id, conversation_history):
    conversation_histories[session_id] = conversation_history
    
def get_conversation_history(session_id):
    return conversation_histories.get(session_id, [])

def interact_with_gpt4(user_input, session_id):
    # Retrieve the conversation history for the session
    conversation_history = get_conversation_history(session_id)

    # Add the context as a system message
    conversation_history.append({
        'role': 'system',
        'content': overview
    })
    
    # Add the new user input to the history
    conversation_history.append({
        'role': 'user',
        'content': user_input
    })


    # Generate the GPT-4 response
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=conversation_history
    )
    response = completion.choices[0].message.content

    # Update the conversation history with the response
    conversation_history.append({
        'role': 'assistant',
        'content': response
    })

    # Save the updated conversation history
    save_conversation_history(session_id, conversation_history)

    return response

def test_function(input):
    return input
    
def read_text_from_file(file_path):
    """
    Reads text from a file.

    :param file_path: Path to the text file.
    :return: String containing the text from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        return contents
    except Exception as e:
        # Handle any exceptions, such as file not found, read errors, etc.
        return str(e)

def truncate_text(text, word_limit=7000):
    """
    Truncate the text to the specified number of words.

    :param text: String containing the original text.
    :param word_limit: Maximum number of words to keep.
    :return: Truncated text.
    """
    words = text.split()
    return ' '.join(words[:word_limit])

def generate_flashcards(text, num_flashcards, model_name="gpt-4-1106-preview"):
    """
    Generates a specified number of flashcards from the provided text using the specified OpenAI model.

    :param text: String containing the text from which to generate flashcards.
    :param num_flashcards: Number of flashcards to generate.
    :param model_name: The name of the OpenAI model to use.
    :return: List of flashcards in the specified format.
    """

    openai.api_key = ' API Key '  # Replace with your actual OpenAI API key

    # Prepare the chat completion request
    messages = [
        {"role": "system", "content": f"""
                  Summarize the text provided then extract key concepts. Then create flashcards and put them in a JSON file following this format:
                    {
                      {"term": "[Key Concept 1]", "explanation": "[Explanation of Key Concept 1]"},
                      {"term": "[Key Concept 2]", "explanation": "[Explanation of Key Concept 2]"},
                      ...
                    }

                    Create {num_flashcards}. Make sure to always return a JSON file.
                """},
        {"role": "user", "content": text}]

    response = openai.chat.completions.create(
        model=model_name,
        response_format={ "type": "json_object" },
        messages=messages
    )
        
    return response.choices[0].message.content


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['fileToUpload']
    num_flashcards = request.form.get('numberField')
    if file:
        filename = secure_filename(file.filename)

        static_folder_path = os.path.join(app.root_path, 'static')

        os.makedirs(static_folder_path, exist_ok=True)

        file_save_path = os.path.join(static_folder_path, filename)

        file.save(file_save_path)

        # Call your function with the file
        text_input = read_text_from_file(file_save_path)
        truncated_text = truncate_text(text_input)
        flashcards = generate_flashcards(truncated_text, num_flashcards)

        data = json.loads(flashcards)

        # Optionally, remove the file if it's no longer needed
        os.remove(file_save_path)

        # Return the result of your function
        return jsonify(data)
    else:
        return 'No file selected'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_notes', methods=['POST'])
def process_notes():
    data = request.get_json()
    lecture_notes = data['notes']
    num_flashcards = int(data['number'])

    truncated_text = truncate_text(lecture_notes)
    flashcards = generate_flashcards(truncated_text, num_flashcards)

    data = json.loads(flashcards)

    return jsonify(data)

@app.route('/process_string', methods=['POST'])
def process_string():
    data = request.json
    input_string = data['input1']
    session_id = data['input2']
    output_string = interact_with_gpt4(input_string, session_id)
    return jsonify({"output": output_string})


if __name__ == '__main__':
    app.run(debug=True)

