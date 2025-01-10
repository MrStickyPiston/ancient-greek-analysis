fn logos() {
    let new_conjugation_nominative_singular = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Nominative as i32),
        suffix: ActiveValue::Set(Option::from("ος".to_owned())),
        ..Default::default()
    };

    let new_conjugation_genitive_singular = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Genitive as i32),
        suffix: ActiveValue::Set(Option::from("ου".to_owned())),
        ..Default::default()
    };

    let new_conjugation_dative_singular = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Dative as i32),
        suffix: ActiveValue::Set(Option::from("ῳ".to_owned())),
        ..Default::default()
    };

    let new_conjugation_accusative_singular = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Accusative as i32),
        suffix: ActiveValue::Set(Option::from("ον".to_owned())),
        ..Default::default()
    };

    let new_conjugation_vocative_singular = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Singular as i32),
        morphological_case: ActiveValue::Set(Case::Vocative as i32),
        suffix: ActiveValue::Set(Option::from("ε".to_owned())),
        ..Default::default()
    };

    let new_conjugation_nominative_dual = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Dual as i32),
        morphological_case: ActiveValue::Set(Case::Nominative as i32),
        suffix: ActiveValue::Set(Option::from("ω".to_owned())),
        ..Default::default()
    };

    let new_conjugation_genitive_dual = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Dual as i32),
        morphological_case: ActiveValue::Set(Case::Genitive as i32),
        suffix: ActiveValue::Set(Option::from("ων".to_owned())),
        ..Default::default()
    };

    let new_conjugation_dative_dual = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Dual as i32),
        morphological_case: ActiveValue::Set(Case::Dative as i32),
        suffix: ActiveValue::Set(Option::from("οιν".to_owned())),
        ..Default::default()
    };

    let new_conjugation_accusative_dual = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Dual as i32),
        morphological_case: ActiveValue::Set(Case::Accusative as i32),
        suffix: ActiveValue::Set(Option::from("ω".to_owned())),
        ..Default::default()
    };

    let new_conjugation_nominative_plural = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Plural as i32),
        morphological_case: ActiveValue::Set(Case::Nominative as i32),
        suffix: ActiveValue::Set(Option::from("οι".to_owned())),
        ..Default::default()
    };

    let new_conjugation_genitive_plural = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Plural as i32),
        morphological_case: ActiveValue::Set(Case::Genitive as i32),
        suffix: ActiveValue::Set(Option::from("ων".to_owned())),
        ..Default::default()
    };

    let new_conjugation_dative_plural = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Plural as i32),
        morphological_case: ActiveValue::Set(Case::Dative as i32),
        suffix: ActiveValue::Set(Option::from("οις".to_owned())),
        ..Default::default()
    };

    let new_conjugation_accusative_plural = noun_conjugation_table::ActiveModel {
        conjugation_group: ActiveValue::Set("λόγος".to_owned()),
        morphological_amount: ActiveValue::Set(Amount::Plural as i32),
        morphological_case: ActiveValue::Set(Case::Accusative as i32),
        suffix: ActiveValue::Set(Option::from("ους".to_owned())),
        ..Default::default()
    };

    for conjugation in vec![
        new_conjugation_nominative_singular,
        new_conjugation_genitive_singular,
        new_conjugation_dative_singular,
        new_conjugation_accusative_singular,
        new_conjugation_vocative_singular,
        new_conjugation_nominative_dual,
        new_conjugation_genitive_dual,
        new_conjugation_dative_dual,
        new_conjugation_accusative_dual,
        new_conjugation_nominative_plural,
        new_conjugation_genitive_plural,
        new_conjugation_dative_plural,
        new_conjugation_accusative_plural,
    ] {
        conjugation.save(&db).await?;
    }
}