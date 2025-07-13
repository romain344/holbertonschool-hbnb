from app.models.user import User

def test_user_creation():
    print("Test de création d'un utilisateur avec mot de passe sécurisé...")
    user = User("Alice", "Durand", "motdepasse123", "alice@example.com")
    
    assert user.first_name == "Alice"
    assert user.last_name == "Durand"
    assert user.email == "alice@example.com"
    assert user.password is None
    print("✔️ Utilisateur créé avec succès (mot de passe non exposé).")

def test_password_hashing_and_verification():
    print("Test du hachage et de la vérification du mot de passe...")
    user = User("Bob", "Martin", "superSecret", "bob@example.com")
    
    assert user.verify_password("superSecret") == True
    assert user.verify_password("mauvais") == False
    print("✔️ Mot de passe vérifié avec succès (hachage OK).")

def test_email_uniqueness():
    print("Test de l'unicité des emails...")
    user1 = User("Jean", "Dupont", "mdp123", "jean@example.com")
    try:
        user2 = User("Jean2", "Dupont2", "mdp1234", "jean@example.com")
        assert False, "Le système aurait dû empêcher un email en double."
    except ValueError as ve:
        print(f"Erreur attendue capturée : {ve}")

if __name__ == '__main__':
    test_user_creation()
    test_password_hashing_and_verification()
    test_email_uniqueness()