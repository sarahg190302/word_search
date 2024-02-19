from search.models import Paragraph, Word, WordParagraphMap
from django.db import transaction
import custom_errors
from search.validators import AddParagraphValidator, ListTopParagraphValidator

def add_paragraphs(text):
    '''
    Extract paragraphs from text and store it. 
    For each paragraph, store word to paragraph mapping along with word count
    '''
    validator = AddParagraphValidator(data={"text": text})
    validator.is_valid(raise_exception=True)
    text = validator.validated_data["text"]
    text = text.strip()
    paras = text.split("\n\n")
    with transaction.atomic():
        word_to_para_map = {}
        for para in paras:
            # ignore empty paragraph
            if len(para) == 0:
                continue
            paragraph_model = Paragraph(paragraph=para)
            paragraph_model.save()
            words = para.split(" ")
            # create a word_id to paragraph_id map where every combination records the word count
            for word in words:
                # ignore empty word
                if len(word) == 0:
                    continue
                word = word.lower()
                word_model,_ = Word.objects.get_or_create(word=word)
                
                if word_model.id not in word_to_para_map:
                    word_to_para_map[word_model.id] = {}
                if paragraph_model.id not in word_to_para_map[word_model.id]:
                    word_to_para_map[word_model.id][paragraph_model.id] = 0
                word_to_para_map[word_model.id][paragraph_model.id]+=1

        for word_id in word_to_para_map:
            for para_id in word_to_para_map[word_id]:
                WordParagraphMap.objects.create(
                    word_id=word_id, 
                    paragraph_id=para_id, 
                    count=word_to_para_map[word_id][para_id]
                )

def list_top_paragraphs(word, top_n):
    '''
    Lists the top n paragraphs for a given word
    '''
    validator = ListTopParagraphValidator(data={"word": word, "top_n": top_n})
    validator.is_valid(raise_exception=True)
    word = validator.validated_data["word"]
    top_n = validator.validated_data["top_n"]
    try:
        word_model  = Word.objects.get(word=word)
    except Word.DoesNotExist:
        raise custom_errors.WordNotFound()
    paras = list(WordParagraphMap.objects.filter(word=word_model).order_by("-count")[:top_n].values_list("paragraph__paragraph", flat=True))
    return paras
