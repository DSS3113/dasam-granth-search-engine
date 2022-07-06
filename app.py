import os, platform
from flask import Flask, render_template, request, url_for
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import aliased
from flask_sqlalchemy import SQLAlchemy
from to_unicode import to_unicode
from to_ascii import to_ascii

app = Flask(__name__)

"""
Database interface setup begins 
"""

db = SQLAlchemy(app)

db_path =  "sqlite:///" + os.path.dirname(os.path.abspath(__file__)) + r"\database\database.sqlite"
if platform.system != 'Windows':
    db_path = db_path.replace(r'\database\database.sqlite', '/database/database.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = db_path

# Reflect the tables
db.reflect()

# Mapped classes are now created with names by default matching that of the table name.
class Banis(db.Model):
    __tablename__ = 'banis'
class Bani_lines(db.Model):
    __tablename__ = 'bani_lines'
class Compositions(db.Model):
    __tablename__ = 'compositions'
class Languages(db.Model):
    __tablename__ = 'languages'
class Lines(db.Model):
    __tablename__ = 'lines'
class Line_content(db.Model):
    __tablename__ = 'line_content'
class Line_types(db.Model):
    __tablename__ = 'line_types'
class Languages(db.Model):
    __tablename__ = 'languages'
class Sections(db.Model):
    __tablename__ = 'sections'
class Shabads(db.Model):
    __tablename__ = 'shabads'
class Sources(db.Model):
    __tablename__ = 'sources'
class Subsections(db.Model):
    __tablename__ = 'subsections'
class Translation_sources(db.Model):
    __tablename__ = 'translation_sources'
class Translations(db.Model):
    __tablename__ = 'translations'
class Transliterations(db.Model):
    __tablename__ = 'transliterations'
class Writers(db.Model):
    __tablename__ = 'writers'

db_session = db.session

"""
Database interface setup ends 
"""

"""
Template functions begin
"""

@app.route('/')
def index():
       return render_template('index.html')

@app.route('/read_page_by_page', methods=['GET'])
def read_page_by_page():
    source_page = request.args.get('page_no') if request.args.get('page_no') else 1
    transliteration_latin = aliased(Transliterations)
    transliteration_devanagiri = aliased(Transliterations)
    lines_data = db_session.query(
            Line_content.gurmukhi,
            transliteration_devanagiri.transliteration,
            transliteration_latin.transliteration,
            Translations.translation
        ).\
        select_from(Lines).\
        join(Shabads).join(Line_content).join(Translations).join(transliteration_latin).join(transliteration_devanagiri).\
        filter(
            Shabads.composition_id == 2, # Composition id for shabads from Dasam Granth is 2
            Lines.source_page == source_page,
            transliteration_devanagiri.language_id == 4, # Language id for Devanagiri transliteration is 4
            transliteration_latin.language_id == 1, # Language id for Latin transliteration is 1
            Translations.translation_source_id == 7
        ).all()
    #print(request.args.get('highlight'))
    return render_template('read_page_by_page.html', lines_data=lines_data, page_no=source_page, highlight=request.args.get('highlight'), to_unicode=to_unicode)

@app.route('/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/search_results/<int:page_no>', methods=['GET', 'POST'])
def search_results(page_no=1):
    transliteration_latin = aliased(Transliterations)
    transliteration_devanagiri = aliased(Transliterations)
    query = db_session.query(
            Lines.source_page,
            Line_content.gurmukhi,
            transliteration_devanagiri.transliteration,
            transliteration_latin.transliteration,
            Translations.translation,
        ).\
        select_from(Lines).\
        join(Shabads).join(Line_content).join(Translations).join(transliteration_latin).join(transliteration_devanagiri).\
        filter(
            Shabads.composition_id == 2, # Composition id for shabads from Dasam Granth is 2
            transliteration_devanagiri.language_id == 4, # Language id for Devanagiri transliteration is 4
            transliteration_latin.language_id == 1, # Language id for Latin transliteration is 1
            Translations.translation_source_id == 7,
        )
    column_to_match = Translations.translation
    if request.args.get('lang_script') == 'english':
        column_to_match = Translations.translation
    elif request.args.get('lang_script') == 'gurmukhi':
        column_to_match = Line_content.gurmukhi
    elif request.args.get('lang_script') == 'devanagiri':
        column_to_match = transliteration_devanagiri.transliteration
    elif request.args.get('lang_script') == 'transliteration':
        column_to_match = transliteration_latin.transliteration

    # Creating a query to find matches

    if request.args.get('search_phrase'):
        if(request.args.get('lang_script') == 'gurmukhi'):
            query = query.filter(column_to_match.op('regexp')(fr".*{to_ascii(request.args.get('search_phrase'))}.*"))
        elif(request.args.get('lang_script') == 'devanagiri'):
            query = query.filter(column_to_match.op('regexp')(fr".*{to_ascii(request.args.get('search_phrase'))}.*"))
        elif(request.args.get('lang_script') == 'transliteration'):
            query = query.filter(column_to_match.like(f"%{request.args.get('search_phrase')}%"))
        else:
            query = query.filter(column_to_match.like(f"%{request.args.get('search_phrase')}%"))
    
    if request.args.get('begin_with'):
        if(request.args.get('lang_script') != 'gurmukhi'):
            query = query.filter(column_to_match.like(f"{request.args.get('begin_with')}%"))
        else:
            query = query.filter(column_to_match.like(f"{to_ascii(request.args.get('begin_with'))}%"))

    if request.args.get('all'):
        all_words_included_expr = []
        if(request.args.get('lang_script') != 'gurmukhi'):
            for word in request.args.get('all').split(' '):
                all_words_included_expr.append(column_to_match.like(f'%{word}%'))
        else:
            for word in request.args.get('all').split(' '):
                all_words_included_expr.append(column_to_match.like(f'%{to_ascii(word)}%'))
        query = query.filter(and_(*all_words_included_expr)) 

    if request.args.get('first_letters'):
        if request.args.get('lang_script') == 'gurmukhi':
            query = query.filter(Line_content.first_letters.op('regexp')(fr".*{to_ascii(request.args.get('first_letters'))}.*"))
        elif request.args.get('lang_script') == 'devanagiri':
            query = query.filter(transliteration_devanagiri.first_letters.op('regexp')(fr".*{to_ascii(request.args.get('first_letters'))}.*"))
        elif request.args.get('lang_script') == 'transliteration':
            query = query.filter(transliteration_latin.first_letters.op('regexp')(fr".*{request.args.get('first_letters')}.*"))
        else:
            first_letters_regex = r'[ ]?'
            for letter in request.args.get('first_letters'):
                if letter != request.args.get('first_letters')[-1]:
                    first_letters_regex += fr'[{letter.upper()}{letter.lower()}][^ ]*[ ]'
                else:
                    first_letters_regex += fr'[{letter.upper()}{letter.lower()}].*'
            query = query.filter(column_to_match.op('regexp')(first_letters_regex))

    if request.args.get('any'):
        any_words_included_expr = []
        if(request.args.get('lang_script') != 'gurmukhi'):
            for word in request.args.get('all').split(' '):
                any_words_included_expr.append(column_to_match.like(f'%{word}%'))
        else:
            for word in request.args.get('all').split(' '):
                any_words_included_expr.append(column_to_match.like(f'%{to_ascii(word)}%'))
        query = query.filter(or_(*any_words_included_expr)) 

    if request.args.get('exact_phrase'):
        if(request.args.get('lang_script') != 'gurmukhi'):
            query = query.filter(func.lower(column_to_match) == func.lower(request.args.get('exact_phrase')))
        else:
            query = query.filter(column_to_match == to_ascii(request.args.get('exact_phrase')))

    lines_data = query.paginate(page=page_no, per_page=int(request.args.get('results_per_page')) if request.args.get('results_per_page') else 500, error_out=False)

    return render_template('search_results.html', lines_data=lines_data, to_unicode=to_unicode)

"""
Template functions end
"""

if __name__ == '__main__':
    app.run(debug=True)
