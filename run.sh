NOW=$(date +'%Y_%m_%d__%H_%M_%Z')

PARSED_TEXTS_DIR='../resource/sample_texts/small'
NGRAM=3
THRESHOLD=5

python -m main \
    --text_dir $PARSED_TEXTS_DIR \
    --ngram $NGRAM