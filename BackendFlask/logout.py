
#USER LOGOUT
@app.route('/logout', methods=['GET','POST'])
def logout():
    return jsonify({'message': 'You have been logged out.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
