import re

def preprocessing():
    '''
        We do the following:

        1. Read in the text and split into the three canticles
        2. remove canti headings and irrelevant text e.g. Canto XX
        3. Remove numbers and punctuation
        4. convert to lower case
    '''
    # Load the text
    with open('divine_comedy.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Define patterns to identify canticles
    inferno_pattern = r'INFERNO'
    purgatorio_pattern = r'PURGATORIO'
    paradiso_pattern = r'PARADISO'

    # Split the text into canticles
    inferno_text = re.split(inferno_pattern, text)[1]
    inferno_text = re.split(purgatorio_pattern, inferno_text)[0]
    purgatorio_text = re.split(purgatorio_pattern, text)[1]
    purgatorio_text = re.split(paradiso_pattern, purgatorio_text)[0]
    paradiso_text = re.split(paradiso_pattern, text)[1]


    # Function to clean and format the canticle text
    def preprocess_canticle(canticle_text):
        # Remove Roman numeral canto headings
        canticle_text = re.sub(r'\bCanto\s+[IVXLCDM]+\b', '', canticle_text, flags=re.IGNORECASE)
        # Replace multiple spaces or newlines with a standard three-line break between canti
        canticle_text = re.sub(r'\s*\n\s*\n\s*', '\n\n\n', canticle_text)
        # Remove any leftover headers or irrelevant text
        canticle_text = re.sub(r'INFERNO|PURGATORIO|PARADISO', '', canticle_text, flags=re.IGNORECASE)
        # Strip extra whitespace at the start or end of the text
        # Remove punctuation and numbers
        canticle_text = re.sub(r'[^\w\s]', '', canticle_text)
        canticle_text = re.sub(r'\d+', '', canticle_text)
        # Convert to lowercase
        canticle_text = canticle_text.lower()
        return canticle_text.strip()

    inferno_clean = preprocess_canticle(inferno_text)
    purgatorio_clean = preprocess_canticle(purgatorio_text)
    paradiso_clean = preprocess_canticle(paradiso_text)

    whole_clean = inferno_clean + ' ' + purgatorio_clean + ' ' + paradiso_clean

    return inferno_clean, purgatorio_clean, paradiso_clean, whole_clean