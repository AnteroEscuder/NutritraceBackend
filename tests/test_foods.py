from app.models.food import Food


def create_system_food(db_session, name="Arroz blanco cocido"):
    food = Food(
        name=name,
        calories=130,
        protein=2.7,
        carbs=28,
        fat=0.3,
        user_id=None,
        is_system=True,
    )
    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)
    return food


def test_create_list_search_update_and_delete_food(client, auth_headers):
    headers = auth_headers()

    create_response = client.post(
        "/foods/",
        headers=headers,
        json={
            "name": "Avena",
            "calories": 389,
            "protein": 16.9,
            "carbs": 66.3,
            "fat": 6.9,
            "allergen_ids": [],
        },
    )

    assert create_response.status_code == 201
    food = create_response.json()
    assert food["name"] == "Avena"
    assert food["allergens"] == []

    list_response = client.get("/foods/?search=ave", headers=headers)
    assert list_response.status_code == 200
    assert [item["name"] for item in list_response.json()] == ["Avena"]

    update_response = client.put(
        f"/foods/{food['id']}",
        headers=headers,
        json={
            "name": "Avena integral",
            "calories": 390,
            "protein": 17,
            "carbs": 67,
            "fat": 7,
            "allergen_ids": [],
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Avena integral"

    delete_response = client.delete(f"/foods/{food['id']}", headers=headers)
    assert delete_response.status_code == 204
    assert client.get("/foods/", headers=headers).json() == []


def test_foods_are_scoped_to_current_user(client, auth_headers):
    ana_headers = auth_headers(email="ana@example.com", name="Ana")
    bob_headers = auth_headers(email="bob@example.com", name="Bob")

    create_response = client.post(
        "/foods/",
        headers=ana_headers,
        json={
            "name": "Yogur",
            "calories": 61,
            "protein": 3.5,
            "carbs": 4.7,
            "fat": 3.3,
            "allergen_ids": [],
        },
    )
    food_id = create_response.json()["id"]

    assert client.get("/foods/", headers=ana_headers).json()[0]["name"] == "Yogur"
    assert client.get("/foods/", headers=bob_headers).json() == []

    bob_update = client.put(
        f"/foods/{food_id}",
        headers=bob_headers,
        json={
            "name": "Yogur editado",
            "calories": 80,
            "protein": 4,
            "carbs": 5,
            "fat": 4,
            "allergen_ids": [],
        },
    )
    assert bob_update.status_code == 404


def test_food_name_must_be_unique_per_user(client, auth_headers):
    headers = auth_headers()
    payload = {
        "name": "Arroz",
        "calories": 130,
        "protein": 2.7,
        "carbs": 28,
        "fat": 0.3,
        "allergen_ids": [],
    }

    assert client.post("/foods/", headers=headers, json=payload).status_code == 201
    response = client.post("/foods/", headers=headers, json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Ya tienes un alimento con ese nombre"


def test_system_foods_are_visible_but_not_editable(client, auth_headers, db_session):
    headers = auth_headers()
    system_food = create_system_food(db_session)

    list_response = client.get("/foods/", headers=headers)

    assert list_response.status_code == 200
    assert list_response.json()[0]["name"] == "Arroz blanco cocido"
    assert list_response.json()[0]["is_system"] is True

    update_response = client.put(
        f"/foods/{system_food.id}",
        headers=headers,
        json={
            "name": "Arroz cambiado",
            "calories": 150,
            "protein": 3,
            "carbs": 30,
            "fat": 1,
            "allergen_ids": [],
        },
    )
    delete_response = client.delete(f"/foods/{system_food.id}", headers=headers)

    assert update_response.status_code == 404
    assert delete_response.status_code == 404


def test_meals_can_use_system_foods_but_not_other_users_foods(client, auth_headers, db_session):
    ana_headers = auth_headers(email="ana@example.com", name="Ana")
    bob_headers = auth_headers(email="bob@example.com", name="Bob")
    system_food = create_system_food(db_session, name="Pechuga de pollo")

    system_meal = client.post(
        "/meals/",
        headers=ana_headers,
        json={"food_id": system_food.id, "quantity": 100, "date": "2026-05-16"},
    )

    assert system_meal.status_code == 201
    assert system_meal.json()["food_name"] == "Pechuga de pollo"

    own_food = client.post(
        "/foods/",
        headers=ana_headers,
        json={
            "name": "Receta privada",
            "calories": 250,
            "protein": 10,
            "carbs": 20,
            "fat": 12,
            "allergen_ids": [],
        },
    ).json()

    bob_meal = client.post(
        "/meals/",
        headers=bob_headers,
        json={"food_id": own_food["id"], "quantity": 100, "date": "2026-05-16"},
    )

    assert bob_meal.status_code == 404
    assert bob_meal.json()["detail"] == "Alimento no encontrado"
