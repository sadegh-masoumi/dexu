import re
from django.core.exceptions import ValidationError
from .models import Node, Relation


def process_user_relations(username: str, raw_data: str) -> dict:
    """
    Creates or updates relations from the given data.
    Returns a structured dictionary with the origin, list of created/updated relations, and count.
    """
    origin_node, _ = Node.objects.get_or_create(name=username)
    found_usernames = set(re.findall(r'@(\w+)', raw_data))

    relations_result = []

    for uname in found_usernames:
        if uname == username:
            continue

        destination_node, _ = Node.objects.get_or_create(name=uname)

        try:
            relation, created = Relation.objects.get_or_create(
                origin=origin_node,
                destination=destination_node,
                defaults={'weight': 1}
            )

            if created:
                relations_result.append(f"{origin_node.name} -> {destination_node.name} (new)")
            else:
                relation.weight += 1
                relation.save()
                relations_result.append(f"{origin_node.name} -> {destination_node.name} (updated)")

        except ValidationError:
            continue

    return {
        "origin": origin_node.name,
        "relations_created": relations_result,
        "destination_count": len(relations_result)
    }
