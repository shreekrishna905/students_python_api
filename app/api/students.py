from app.api import bp
from flask import jsonify
from app.models import Student
from flask import request
from app import db
from flask import url_for
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/students', methods=['GET'])
@token_auth.login_required
def get_students():
    students = Student.query.all()
    return jsonify({'students': [s.to_dict() for s in students]})


@bp.route('/students/<int:id>', methods=['GET'])
@token_auth.login_required
def get_student(id):
    return jsonify(Student.query.get_or_404(id).to_dict())


@bp.route('/students', methods=['POST'])
@token_auth.login_required
def create_student():
    data = request.get_json() or {}
    if 'name' not in data or 'email' not in data:
        return bad_request('must include name, email')
    if Student.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    student = Student(name=data['name'], phone=data['phone'], email=data['email'])
    db.session.add(student)
    db.session.commit()
    response = jsonify(student.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_students', id=student.id)
    return response


@bp.route('/students/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' not in data or 'email' not in data:
        return bad_request('must include name, email')
    if data['email'] != student.email and Student.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    student = Student(name=data['name'], phone=data['phone'], email=data['email'])
    db.session().commit()
    return jsonify(student.to_dict())
