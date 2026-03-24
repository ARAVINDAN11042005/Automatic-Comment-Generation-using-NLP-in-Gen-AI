from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, save_submission, get_all_submissions, get_submission_by_id, delete_submission, get_aggregate_metrics
from models.nlp_model import NLPCommentGenerator
from models.alsi_model import ALSICommentGenerator
from models.chatbot_model import CodeFixerChatbot
from utils.metrics import generate_simulated_metrics, get_overall_comparison

app = Flask(__name__)
CORS(app)

# Initialize models
nlp_model = NLPCommentGenerator()
alsi_model = ALSICommentGenerator()
chatbot_model = CodeFixerChatbot()

# Initialize database
init_db()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Comment Generation API is running'})

@app.route('/api/generate', methods=['POST'])
def generate_comments():
    """Generate comments using both NLP and ALSI models."""
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'Code input is required'}), 400
    
    code = data['code']
    language = data.get('language', 'python')
    
    # Generate comments from both models
    nlp_result = nlp_model.generate_comment(code, language)
    alsi_result = alsi_model.generate_comment(code, language)
    
    # Calculate metrics
    metrics = generate_simulated_metrics(code, nlp_result['comment'], alsi_result['comment'])
    
    # Save to database
    submission_data = {
        'code_input': code,
        'language': language,
        'nlp_comment': nlp_result['comment'],
        'alsi_comment': alsi_result['comment'],
        'nlp_score': nlp_result['confidence'],
        'alsi_score': alsi_result['confidence'],
        'nlp_bleu': metrics['nlp']['bleu'],
        'alsi_bleu': metrics['alsi']['bleu'],
        'nlp_precision': metrics['nlp']['precision'],
        'alsi_precision': metrics['alsi']['precision'],
        'nlp_recall': metrics['nlp']['recall'],
        'alsi_recall': metrics['alsi']['recall'],
        'nlp_f1': metrics['nlp']['f1'],
        'alsi_f1': metrics['alsi']['f1'],
    }
    
    submission_id = save_submission(submission_data)
    
    return jsonify({
        'id': submission_id,
        'code': code,
        'language': language,
        'nlp': {
            **nlp_result,
            'metrics': metrics['nlp']
        },
        'alsi': {
            **alsi_result,
            'metrics': metrics['alsi']
        }
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all past submissions."""
    submissions = get_all_submissions()
    return jsonify({'submissions': submissions, 'total': len(submissions)})

@app.route('/api/history/<int:submission_id>', methods=['GET'])
def get_single_submission(submission_id):
    """Get a specific submission by ID."""
    submission = get_submission_by_id(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    return jsonify(submission)

@app.route('/api/history/<int:submission_id>', methods=['DELETE'])
def remove_submission(submission_id):
    """Delete a submission."""
    delete_submission(submission_id)
    return jsonify({'message': 'Submission deleted successfully'})

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get aggregate metrics from all submissions."""
    db_metrics = get_aggregate_metrics()
    overall = get_overall_comparison()
    return jsonify({
        'database_metrics': db_metrics,
        'research_metrics': overall
    })

@app.route('/api/compare', methods=['POST'])
def compare_models():
    """Compare both models on a given code input."""
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'Code input is required'}), 400
    
    code = data['code']
    language = data.get('language', 'python')
    
    nlp_result = nlp_model.generate_comment(code, language)
    alsi_result = alsi_model.generate_comment(code, language)
    metrics = generate_simulated_metrics(code, nlp_result['comment'], alsi_result['comment'])
    
    return jsonify({
        'nlp': {**nlp_result, 'metrics': metrics['nlp']},
        'alsi': {**alsi_result, 'metrics': metrics['alsi']},
        'overall_comparison': get_overall_comparison()
    })

@app.route('/api/fix-code', methods=['POST'])
def fix_code_endpoint():
    """Fix common coding mistakes for the Chatbot."""
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'Code input is required'}), 400
    
    code = data['code']
    language = data.get('language', 'python')
    
    result = chatbot_model.fix_code(code, language)
    return jsonify(result)

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about both models."""
    return jsonify({
        'nlp': nlp_model.get_model_info(),
        'alsi': alsi_model.get_model_info()
    })

if __name__ == '__main__':
    print("[*] Starting Comment Generation API Server...")
    print("[+] NLP Model loaded successfully")
    print("[+] ALSI Model loaded successfully")
    print("[+] Database initialized")
    app.run(debug=True, port=5000)
