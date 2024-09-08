connection: "external_small"

### Owner - Tal ###

include: "/**/*.view.lkml"                 # include all views in this project
include: "/**/*.dashboard.lookml"   # include a LookML dashboard called my_dashboard

week_start_day: sunday

# Explores
# Policy Checkout Details
explore: dima_table {
access_filter: {field: dima_table.merchant_id
                  user_attribute: merchant_id_new}
  access_filter: {field: dima_table.order_id
                  user_attribute: dima
                  }
}