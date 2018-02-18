#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TypePerson:

    def __init__(prenom, nom, entreprises):
        self.tweet_id = idd
        self.tweet_created_at = date
        self.tweet_text = text
        self.hashtags   = tags
        self.tweet_quoted_status_id = quotedId
        self.tweet_mention = mention
        self.pertinent = pertinent
        self.proba_pertinence = p
        self.user_id = userId
        self.user_screenname  = userScreenname
        self.user_name = userName
        self.user_location = userLocation
        self.user_description = userDescription

        """ Parametre supplementaire pour les cas personnes, on separe le nom et le prenom """
        self.userSurname = nom
        self.userFirstname = prenom

        """ Parametre supplementaire, trois types d'auteurs: PERSON, INDETERMINED, COMPANY. """
        self.typeAuteur = typeAuteur